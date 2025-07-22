# MIT License - Copyright (c) 2025 Robert Cole

from btpie import utils
from datetime import datetime

def test_hex_dump():
    data = b'\x01\x02\xAA\xFF'
    expected = '01 02 AA FF'

    result = utils.hex_dump(data)
    
    assert result == expected

def test_timestamp_format():
    ts = utils.timestamp()
    
    # Validate structure using datetime
    try:
        datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
        valid = True
    except ValueError:
        valid = False

    assert valid, "Timestamp is not in expected format YYYY-MM-DD HH:MM:SS"