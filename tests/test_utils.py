from pylates import utils


def test_find_mac_valid():
    mac_lower_str = 'aa:bb:cc:dd:ee:ff'
    mac_lower = utils.find_mac_address(mac_lower_str)
    assert mac_lower == mac_lower_str

    mac_upper_str = 'AA:BB:CC:DD:EE:FF'
    mac_upper = utils.find_mac_address(mac_upper_str)
    assert mac_upper == mac_upper_str

    mac_camel_str = 'aA:bB:cC:dD:eE:fF'
    mac_camel = utils.find_mac_address(mac_camel_str)
    assert mac_camel == mac_camel_str

    mac_dashed_str = 'aa-bb-cc-dd-ee-ff'
    mac_dashed = utils.find_mac_address(mac_dashed_str)
    assert mac_dashed == mac_dashed_str


def test_find_mac_invalid():
    invalid_str = 'This is not a mac!'
    mac_invalid = utils.find_mac_address(invalid_str)
    assert mac_invalid == ''

    invalid_chars_str = 'AR:BB:CC:DD:ES:FF'
    mac_invalid = utils.find_mac_address(invalid_chars_str)
    assert mac_invalid == ''
