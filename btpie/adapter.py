import bluetooth
import time

class BluetoothAdapter:
    def __init__(self, master_mac, slave_mac, port=1):
        self.master_mac = master_mac
        self.slave_mac = slave_mac
        self.port = port
        self.client_sock = None
        self.server_sock = None
        self.conn_sock = None

    def connect_to_slave(self, retries=5, delay=2):
        """Try connecting to the slave/target device (OBD) with retries"""
        attempt = 0
        while attempt < retries:
            try:
                self.client_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                self.client_sock.connect((self.slave_mac, self.port))
                print(f"[+] Connected to slave {self.slave_mac} on port {self.port}")
                return True
            except Exception as e:
                print(f"[!] Slave connection attempt {attempt + 1} failed: {e}")
                attempt += 1
                time.sleep(delay)
        
        print(f"[!] Failed to connect to slave {self.slave_mac} after {retries} attempts")
        return False

    def start_server(self):
        """Start RFCOMM server, accept only authorized master device"""
        self.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.server_sock.bind(("", self.port))
        self.server_sock.listen(1)
        print(f"[+] Waiting for master ({self.master_mac}) to connect on port {self.port}...")

    def wait_for_master(self):
        """Loop until master connects"""
        while True:
            conn_sock, client_info = self.server_sock.accept()
            if client_info[0] == self.master_mac:
                self.conn_sock = conn_sock
                print(f"[+] Accepted connection from master {client_info}")
                return
            else:
                print(f"[!] Rejected connection from unknown device {client_info[0]}")
                conn_sock.close()

    def close(self):
        """Close all sockets"""
        if self.conn_sock:
            self.conn_sock.close()
            self.conn_sock = None
        if self.client_sock:
            self.client_sock.close()
            self.client_sock = None
