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
        self.running = True

    def start(self):
        """Start MITM with reconnect handling"""
        self.logger.info(f"[*] Starting MITM session (Master: {self.master_mac}, Slave: {self.slave_mac})")

        self.adapter.start_server()

        while self.running:
            try:
                self.logger.info("[*] Waiting for master to connect...")
                self.adapter.wait_for_master()

                if not self.adapter.connect_to_slave():
                    self.logger.error("[!] Could not connect to slave, aborting session.")
                    break

                self.logger.info("[*] Relay active. Press CTRL+C to stop.")

                t1 = threading.Thread(target=self.relay, args=(self.adapter.conn_sock, self.adapter.client_sock, "Master → Slave"))
                t2 = threading.Thread(target=self.relay, args=(self.adapter.client_sock, self.adapter.conn_sock, "Slave → Master"))
                t1.start()
                t2.start()
                
                t1.join()
                t2.join()

                self.logger.warning("[!] Connection lost. Restarting listener.")
                self.adapter.close()

            except Exception as e:
                self.logger.error(f"[!] Unexpected error: {e}")
                self.running = False

        self.cleanup()

    def relay(self, source_sock, dest_sock, direction):
        """Relay data with logging"""
        try:
            while True:
                data = source_sock.recv(1024)
                if not data:
                    break
                self.logger.info(f"[{direction}] {data.hex()}")
                dest_sock.send(data)
        except Exception as e:
            self.logger.error(f"[!] Relay error ({direction}): {e}")

    def cleanup(self):
        """Close all sockets"""
        self.logger.info("[*] Cleaning up sockets")
        self.adapter.close()
