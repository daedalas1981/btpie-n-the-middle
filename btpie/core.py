import threading
import time
from btpie.logger import setup_logger
from btpie.adapter import BluetoothAdapter

class MITMCore:
    def __init__(self, master_mac, slave_mac, log_file="logs/session.log"):
        self.master_mac = master_mac
        self.slave_mac = slave_mac
        self.log_file = log_file
        self.logger = setup_logger(self.log_file)
        self.adapter = BluetoothAdapter(master_mac, slave_mac)
        self.running = False

    def start(self):
        """Start the MITM relay"""
        self.logger.info(f"[*] Starting MITM session (Master: {self.master_mac}, Slave: {self.slave_mac})")

        try:
            self.adapter.start_server()      # Wait for master (MotoScan)
            self.adapter.connect_to_slave()  # Connect to slave (OBD)
        except Exception as e:
            self.logger.error(f"[!] Connection setup failed: {e}")
            return

        self.running = True

        threading.Thread(target=self.relay, args=(self.adapter.conn_sock, self.adapter.client_sock, "Master → Slave")).start()
        threading.Thread(target=self.relay, args=(self.adapter.client_sock, self.adapter.conn_sock, "Slave → Master")).start()

    def relay(self, source_sock, dest_sock, direction):
        """Relay data with logging"""
        try:
            while self.running:
                data = source_sock.recv(1024)
                if not data:
                    self.logger.warning(f"[!] Connection closed ({direction})")
                    self.running = False
                    break

                self.logger.info(f"[{direction}] {data.hex()}")
                dest_sock.send(data)
        except Exception as e:
            self.logger.error(f"[!] Relay error ({direction}): {e}")
            self.running = False

        self.cleanup()

    def cleanup(self):
        """Close connections"""
        if self.running:
            self.running = False
            self.logger.info("[*] Cleaning up sockets")
            self.adapter.close()
