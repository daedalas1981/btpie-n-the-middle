# MIT License - Copyright (c) 2025 Robert Cole

import sys
import pytest
from unittest import mock
from btpie.core import MITMCore

def test_version_flag(capsys):
    test_args = ["btpie.py", "--version"]
    with mock.patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit):
            import btpie
            btpie.main()
    captured = capsys.readouterr()
    assert "BTPiE-N-THE-MIDDLE" in captured.out

def test_malformed_flag(capsys):
    test_args = ["btpie.py", "--unknown"]
    with mock.patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit):
            import btpie
            btpie.main()
    captured = capsys.readouterr()
    assert "unrecognized arguments" in captured.err.lower()
    assert "usage: btpie.py" in captured.err

def test_missing_mitm_args(capsys):
    test_args = ["btpie.py", "--mitm"]
    with mock.patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit):
            import btpie
            btpie.main()
    captured = capsys.readouterr()
    assert "Error: --master and --slave required with --mitm" in captured.out

def test_log_flag_sets_filename(tmp_path):
    log_file = tmp_path / "cli_test.log"
    test_args = [
        "btpie.py",
        "--master", "00:11:22:33:44:55",
        "--slave", "AA:BB:CC:DD:EE:FF",
        "--log", str(log_file)
    ]
    with mock.patch.object(sys, "argv", test_args), \
         mock.patch("btpie.MITMCore.run", return_value=None):
        import btpie
        btpie.main()
    assert log_file.exists()

def test_port_and_verbose_flags():
    test