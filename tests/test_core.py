# MIT License - Copyright (c) 2025 Robert Cole

import pytest
from btpie.core import MITMCore
from btpie import main

def test_mitmcore_initialization():
    mitm = MITMCore(
        master_mac="00:11:22:33:44:55",
        slave_mac="AA:BB:CC:DD:EE:FF",
        log_file="logs/test.log",
        port=5,
        verbose=True
    )

    assert mitm.master_mac == "00:11:22:33:44:55"
    assert mitm.slave_mac == "AA:BB:CC:DD:EE:FF"
    assert mitm.log_file == "logs/test.log"
    assert mitm.port == 5
    assert mitm.verbose is True
    assert mitm.adapter.master_mac == "00:11:22:33:44:55"
    assert mitm.adapter.slave_mac == "AA:BB:CC:DD:EE:FF"
    assert mitm.adapter.port == 5
    assert mitm.stop_event.is_set() is False

def test_mitmcore_cleanup_sets_stop():
    mitm = MITMCore(
        master_mac="11:22:33:44:55:66",
        slave_mac="77:88:99:AA:BB:CC"
    )

    mitm.cleanup()

    assert mitm.stop_event.is_set() is True
