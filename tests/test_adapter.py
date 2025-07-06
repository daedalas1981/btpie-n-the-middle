"""
Basic unit tests for btpie.adapter
"""

import unittest
from btpie.adapter import BluetoothAdapter

class TestBluetoothAdapter(unittest.TestCase):
    
    def test_initialization(self):
        master_mac = "00:04:3E:8F:AF:1F"
        slave_mac = "00:02:1E:8F:AF:3F"
        adapter = BluetoothAdapter(master_mac, slave_mac)
        
        self.assertEqual(adapter.master_mac, master_mac)
        self.assertEqual(adapter.slave_mac, slave_mac)
        self.assertEqual(adapter.port, 1)
        self.assertIsNone(adapter.client_sock)
        self.assertIsNone(adapter.server_sock)
        self.assertIsNone(adapter.conn_sock)

if __name__ == "__main__":
    unittest.main()
