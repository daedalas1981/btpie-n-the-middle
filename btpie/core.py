import threading
import time

from btpie.logger import setup_logger
from btpie.adapter import BluetoothAdapter

class MITMCore:
    def __init__(self, target_mac, log_file="logs/session.log"):
        self.target_mac = target_mac
        self.log_file = log_file
        self.logger = setup_logger(self.log_file)
        self.adapter = BluetoothAdapter(self.target_mac)
        self.running = False

    def start(self):
        """Start the MITM relay"""
        self.logger.info("[*] Starting MITM session")

        try:
            self.adapter.start_server()  # Wait for MotoScan (client) connection
            self.adapter.connect_to_target()  # Connect to OBD (target)
        except Exception as e:
            self.logger.error(f"[!] Failed to establish connections: {e}")
            return

        self.running = True

        threading.Thread(target=self.relay, args=(self.adapter.conn_sock, self.adapter.client_sock, "MotoScan → OBD")).start()
        threading.Thread(target=self.relay, args=(self.adapter.client_sock, self.adapter.conn_sock, "OBD → MotoScan")).start()

    def relay(self, source_sock, dest_sock, direction):
        """Relay data between sockets, with logging"""
        try:
            while self.running:
                data = source_sock.recv(1024)
                if not data:
                    self.logger.warning(f"[!] Connection closed in {direction}")
                    self.running = False
                    break

                self.logger.info(f"[{direction}] {data.hex()}")
                dest_sock.send(data)
        except Exception as e:
            self.logger.error(f"[!] Relay error ({direction}): {e}")
            self.running = False

        self.cleanup()

    def cleanup(self):
        """Tear down all connections"""
        if self.running:
            self.running = False
            self.logger.info("[*] Cleaning up sockets")
            self.adapter.close()
