"""Test network data point class functionality."""

from unittest import mock

from pylates.platform_network_managers import WindowsNetworkManager
from pylates.ssid_data_point import SSIDDataPoint
from tests import test_platform_manager


@mock.patch('subprocess.check_output',
            side_effect=test_platform_manager.get_netsh_fake_data_long)
def test_create_data_point(get_fake_data):
    wnm = WindowsNetworkManager()
    points_data = wnm.gather_networks_info(wnm.CMD_NETSH)
    point = SSIDDataPoint(**points_data[0])
    assert point.ssid == 'SSID number 1'
    assert point.authentication == 'WPA2-Personal'
    assert point.encryption == 'CCMP'
    assert point.network_type == 'Infrastructure'

    assert point.bssid[0].mac_address == '20:ab:4b:ab:a5:ab'
    assert point.bssid[0].signal_quality == 6
    assert point.bssid[0].signal_rssi == -97.0
    assert point.bssid[0].channel == 6
