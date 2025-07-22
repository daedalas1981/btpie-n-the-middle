# MIT License - Copyright (c) 2025 Robert Cole

import sys
import pytest
from unittest import mock
from btpie import MITMCore
import btpie

def test_version_flag(capsys):
    """Test --version flag prints version info."""
    test_args = ["btpie.py", "--version"]
    with mock.patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit):
            btpie.main()
    captured = capsys.readouterr()
    assert "BTPiE-N-THE-MIDDLE" in captured.out

def test_malformed_flag(capsys):
    """Test unknown argument exits with usage error."""
    test_args = ["btpie.py", "--unknown"]
    with mock.patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit):
            btpie.main()
    captured = capsys.readouterr()
    assert "unrecognized arguments" in captured.err.lower()
    assert "usage: btpie.py" in captured.err

def test_missing_mitm_args(capsys):
    """Test --mitm without --master/--slave triggers error."""
    test_args = ["btpie.py", "--mitm"]
    with mock.patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit):
            btpie.main()
    captured = capsys.readouterr()
    assert "Error: --master and --slave required with --mitm" in captured.out

def test_log_flag_sets_filename(tmp_path):
    """Test --log flag sets log filename."""
    log_file = tmp_path / "cli_test.log"
    test_args = [
        "btpie.py",
        "--master", "00:11:22:33:44:55",
        "--slave", "AA:BB:CC:DD:EE:FF",
        "--log", str(log_file)
    ]
    with mock.patch.object(sys, "argv", test_args), \
         mock.patch("btpie.MITMCore.run", return_value=None):
        btpie.main()
    assert log_file.exists()

def test_port_and_verbose_flags():
    """Test --port and --verbose flags are passed to MITMCore."""
    test_args = [
        "btpie.py",
        "--master", "11:22:33:44:55:66",
        "--slave", "77:88:99:AA:BB:CC",
        "--port", "4",
        "--verbose"
    ]
    with mock.patch.object(sys, "argv", test_args), \
         mock.patch("btpie.MITMCore.run", return_value=None) as mock_run, \
         mock.patch("btpie.MITMCore.__init__", return_value=None) as mock_init:
        btpie.main()
        mock_init.assert_called_with(
            master_mac="11:22:33:44:55:66",
            slave_mac="77:88:99:AA:BB:CC",
            port=4,
            verbose=True,
            log_file="logs/session.log"
        )
        mock_run.assert_called_once()