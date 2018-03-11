"""Test network data point class functionality."""

from unittest import mock

from pylates.platform_network_managers import WindowsNetworkManager
from pylates.ssid_data_point import SSIDDataPoint
from tests import test_platform_manager


def get_fake_time():
    return 1500000000


@mock.patch('subprocess.check_output',
            side_effect=test_platform_manager.get_netsh_fake_data)
@mock.patch('time.time', side_effect=get_fake_time)
def test_create_data_point(get_fake_data, time_func):
    mac_address = '11:22:33:44:55:66'
    location = (0, 1)
    wnm = WindowsNetworkManager()
    points_data = wnm.gather_networks_info(wnm.CMD_NETSH)
    point = SSIDDataPoint(mac_address, location, **points_data[0])
    assert point.measurer_mac_address == mac_address
    assert point.measurer_location == location
    assert point.ssid == 'SSID number 1'
    assert point.authentication == 'WPA2-Personal'
    assert point.encryption == 'CCMP'
    assert point.network_type == 'Infrastructure'
    assert point.timestamp == 1500000000

    assert point.bssid[0].mac_address == '20:ab:4b:ab:a5:ab'
    assert point.bssid[0].signal_quality == 6
    assert point.bssid[0].signal_rssi == -97.0
    assert point.bssid[0].channel == 6
