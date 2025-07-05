import bluetooth
import threading

class BluetoothAdapter:
    def __init__(self, target_mac, port=1):
        self.target_mac = target_mac
        self.port = port
        self.client_sock = None
        self.server_sock = None
        self.conn_sock = None

    def connect_to_target(self):
        """Connect to the remote target device"""
        self.client_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.client_sock.connect((self.target_mac, self.port))
        print(f"[+] Connected to target {self.target_mac} on port {self.port}")

    def start_server(self):
        """Start RFCOMM server to accept incoming connection"""
        self.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.server_sock.bind(("", self.port))
        self.server_sock.listen(1)

        print(f"[+] Waiting for connection on RFCOMM port {self.port}...")
        self.conn_sock, client_info = self.server_sock.accept()
        print(f"[+] Accepted connection from {client_info}")

    def close(self):
        """Close all sockets"""
        if self.conn_sock:
            self.conn_sock.close()
        if self.server_sock:
            self.server_sock.close()
        if self.client_sock:
            self.client_sock.close()
