import bluetooth

class BluetoothAdapter:
    def __init__(self, master_mac, slave_mac, port=1):
        self.master_mac = master_mac
        self.slave_mac = slave_mac
        self.port = port
        self.client_sock = None
        self.server_sock = None
        self.conn_sock = None

    def connect_to_slave(self):
        """Connect to the slave/target device (OBD)"""
        self.client_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.client_sock.connect((self.slave_mac, self.port))
        print(f"[+] Connected to slave {self.slave_mac} on port {self.port}")

    def start_server(self):
        """Start RFCOMM server and accept connection from master (MotoScan)"""
        self.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.server_sock.bind(("", self.port))
        self.server_sock.listen(1)

        print(f"[+] Waiting for master ({self.master_mac}) to connect on RFCOMM port {self.port}...")
        while True:
            conn_sock, client_info = self.server_sock.accept()
            if client_info[0] == self.master_mac:
                self.conn_sock = conn_sock
                print(f"[+] Accepted connection from master {client_info}")
                break
            else:
                print(f"[!] Rejected connection from unknown device {client_info[0]}")
                conn_sock.close()

    def close(self):
        """Close all sockets"""
        if self.conn_sock:
            self.conn_sock.close()
        if self.server_sock:
            self.server_sock.close()
        if self.client_sock:
            self.client_sock.close()
