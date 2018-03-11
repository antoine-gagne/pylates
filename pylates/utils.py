import re


def find_mac_address(input_str):
    """Find mac address in input. Return '' if none."""
    regex = r'([a-fA-F0-9]{2}[:|\-]?){6}'
    match = re.search(regex, input_str)
    if match:
        return match.group(0)
    return ''
