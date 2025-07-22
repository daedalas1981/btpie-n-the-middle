# MIT License - Copyright (c) 2025 Robert Cole

from btpie.adapter import BluetoothAdapter
from unittest.mock import MagicMock

def test_adapter_reset_sockets():
    adapter = BluetoothAdapter(master_mac="11:22:33:44:55:66", slave_mac="77:88:99:AA:BB:CC")

    # Mock all sockets
    adapter.server_sock = MagicMock()
    adapter.client_sock = MagicMock()
    adapter.conn_sock = MagicMock()

    # Call the method under test
    adapter.close()

    # Assert all close calls
    adapter.conn_sock.close.assert_called_once()
    adapter.client_sock.close.assert_called_once()
    adapter.server_sock.close.assert_called_once()