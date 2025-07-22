# MIT License - Copyright (c) 2025 Robert Cole

import sys
import pytest
from unittest import mock
from btpie import MITMCore

def test_version_flag(capsys):
    """Test --version flag prints version info."""
    test_args = ["btpie.py", "--version"]
    with mock.patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit):
            import btpie
            btpie.main()
    captured = capsys.readouterr()
    assert "BTPiE-N-THE-MIDDLE" in captured.out

def test_malformed_flag(capsys):
    """Test unknown argument exits with usage error."""
    test_args = ["btpie.py", "--unknown"]
    with mock.patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit):
            import btpie
            btpie.main()
    captured = capsys.readouterr()
    assert "unrecognized arguments" in captured.err.lower()
    assert "usage: btpie.py" in captured.err

def test_missing_mitm_args(capsys):
    """Test --mitm without --master/--slave triggers error."""
    test_args = ["btpie.py", "--mitm"]
    with mock.patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit):
            import btpie
            btpie.main()
    captured = capsys.readouterr()
    assert "Error: --master and --slave required with --mitm" in captured.out

def test_log_flag():