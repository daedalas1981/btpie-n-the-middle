import pytest
from btpie.adapter import BluetoothAdapter

def test_adapter_initialization():
    adapter = BluetoothAdapter(master_mac="00:11:22:33:44:55", slave_mac="AA:BB:CC:DD:EE:FF", port=3)
    
    assert adapter.master_mac == "00:11:22:33:44:55"
    assert adapter.slave_mac == "AA:BB:CC:DD:EE:FF"
    assert adapter.port == 3
    assert adapter.server_sock is None
    assert adapter.client_sock is None
    assert adapter.conn_sock is None

def test_adapter_default_port():
    adapter = BluetoothAdapter(master_mac="11:22:33:44:55:66", slave_mac="77:88:99:AA:BB:CC")
    
    assert adapter.port == 1

def test_adapter_reset_sockets():
    adapter = BluetoothAdapter(master_mac="11:22:33:44:55:66", slave_mac="77:88:99:AA:BB:CC")
    
    adapter.server_sock = "dummy"
    adapter.client_sock = "dummy"
    adapter.conn_sock = "dummy"
    
    adapter.close()
    
    assert adapter.server_sock is None
    assert adapter.client_sock is None
    assert adapter.conn_sock is None
