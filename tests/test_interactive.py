# MIT License - Copyright (c) 2025 Robert Cole

import subprocess
from unittest import mock
import pytest
import scripts.interactive_btpie as ibp

def test_ensure_bluetooth_on_enabled():
    """Returns True if Bluetooth is already powered on."""
    with mock.patch("subprocess.check_output", return_value="Powered: yes"):
        assert ibp.ensure_bluetooth_on() is True

def test_ensure_bluetooth_on_needs_enable():
    """Calls bluetoothctl to power on when not enabled."""
    with mock.patch("subprocess.check_output", return_value="Powered: no"), \
         mock.patch("subprocess.run", return_value=None) as mock_run:
        assert ibp.ensure_bluetooth_on() is True
        mock_run.assert_called_with(["bluetoothctl", "power", "on"], check=True)

def test_check_paired_true():
    """Returns True if device is marked as paired."""
    with mock.patch("subprocess.getoutput", return_value="Paired: yes"):
        assert ibp.check_paired("00:11:22:33:44:55") is True

def test_check_paired_false():
    """Returns False if device is not marked as paired."""
    with mock.patch("subprocess.getoutput", return_value="Paired: no"):
        assert ibp.check_paired("AA:BB:CC:DD:EE:FF") is False