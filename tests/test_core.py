"""
Basic unit tests for btpie.core
"""

import unittest
from btpie.core import MITMCore

class TestMITMCore(unittest.TestCase):
    
    def test_initialization(self):
        master_mac = "00:04:3E:8F:AF:1F"
        slave_mac = "00:02:1E:8F:AF:3F"
        log_file = "logs/test.log"

        mitm = MITMCore(master_mac, slave_mac, log_file)

        self.assertEqual(mitm.master_mac, master_mac)
        self.assertEqual(mitm.slave_mac, slave_mac)
        self.assertEqual(mitm.log_file, log_file)
        self.assertTrue(hasattr(mitm, "adapter"))
        self.assertTrue(hasattr(mitm, "logger"))
        self.assertTrue(hasattr(mitm, "running"))

if __name__ == "__main__":
    unittest.main()
