from btpie import utils

def test_hex_dump():
    data = b'\x01\x02\xAA\xFF'
    expected = '01 02 AA FF'

    result = utils.hex_dump(data)
    
    assert result == expected

def test_timestamp_format():
    ts = utils.timestamp()
    
    assert isinstance(ts, str)
    assert len(ts) >= 19  # Format: YYYY-MM-DD HH:MM:SS
    assert ts.count(":") == 2
    assert ts.count("-") == 2
