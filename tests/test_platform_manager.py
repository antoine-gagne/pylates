from unittest import mock

from pylates.platform_network_managers import WindowsNetworkManager


def get_netsh_fake_data_long(*args, **kwargs):
    return b"""
Interface name : Wi-Fi
There are 10 networks currently visible.

SSID 1 : SSID number 1
    Network type            : Infrastructure
    Authentication          : WPA2-Personal
    Encryption              : CCMP
    BSSID 1                 : 20:ab:4b:ab:a5:ab
         Signal             : 6%
         Radio type         : 802.11n
         Channel            : 157
         Basic rates (Mbps) : 6 12 24
         Other rates (Mbps) : 9 18 36 48 54
    BSSID 2                 : 20:ab:4b:ab:a5:ab
         Signal             : 30%
         Radio type         : 802.11n
         Channel            : 4
         Basic rates (Mbps) : 1 2 5.5 11
         Other rates (Mbps) : 6 9 12 18 24 36 48 54

SSID 2 : SSID number 2
    Network type            : Infrastructure
    Authentication          : WPA2-Personal
    Encryption              : CCMP
    BSSID 1                 : c8:ab:19:ab:8c:ab
         Signal             : 14%
         Radio type         : 802.11n
         Channel            : 157
         Basic rates (Mbps) : 6 12 24
         Other rates (Mbps) : 9 18 36 48 54
    BSSID 2                 : c8:ab:19:ab:8c:ab
         Signal             : 50%
         Radio type         : 802.11n
         Channel            : 2
         Basic rates (Mbps) : 1 2 5.5 11
         Other rates (Mbps) : 6 9 12 18 24 36 48 54

SSID 3 : SSID number 3 
    Network type            : Infrastructure
    Authentication          : WPA2-Personal
    Encryption              : CCMP
    BSSID 1                 : b0:ab:b9:ab:7d:ab
         Signal             : 80%
         Radio type         : 802.11n
         Channel            : 153
         Basic rates (Mbps) : 6 12 24
         Other rates (Mbps) : 9 18 36 48 54

SSID 4 : SSID number 4
    Network type            : Infrastructure
    Authentication          : WPA2-Personal
    Encryption              : CCMP
    BSSID 1                 : 14:ab:82:ab:27:ab
         Signal             : 0%
         Radio type         : 802.11ac
         Channel            : 36
         Basic rates (Mbps) : 6 12 24
         Other rates (Mbps) : 9 18 36 48 54

SSID 5 : SSID number 5
    Network type            : Infrastructure
    Authentication          : WPA2-Personal
    Encryption              : CCMP
    BSSID 1                 : b0:ab:b9:ab:7d:ab
         Signal             : 87%
         Radio type         : 802.11n
         Channel            : 11
         Basic rates (Mbps) : 1 2 5.5 11
         Other rates (Mbps) : 6 9 12 18 24 36 48 54

SSID 6 : SSID number 6
    Network type            : Infrastructure
    Authentication          : WPA2-Personal
    Encryption              : CCMP
    BSSID 1                 : 00:ab:6a:ab:84:ab
         Signal             : 22%
         Radio type         : 802.11n
         Channel            : 11
         Basic rates (Mbps) : 1 2 5.5 11
         Other rates (Mbps) : 6 9 12 18 24 36 48 54

SSID 7 :
    Network type            : Infrastructure
    Authentication          : Open
    Encryption              : None
    BSSID 1                 : fa:ab:ca:ab:92:ab
         Signal             : 83%
         Radio type         : 802.11n
         Channel            : 2
         Basic rates (Mbps) : 1 2 5.5 11
         Other rates (Mbps) : 6 9 12 18 24 36 48 54

SSID 8 : SSID number 8
    Network type            : Infrastructure
    Authentication          : WPA2-Personal
    Encryption              : CCMP
    BSSID 1                 : 44:ab:dd:ab:a6:ab
         Signal             : 32%
         Radio type         : 802.11n
         Channel            : 6
         Basic rates (Mbps) : 1 2 5.5 11
         Other rates (Mbps) : 6 9 12 18 24 36 48 54

SSID 9 : SSID number 9
    Network type            : Infrastructure
    Authentication          : WPA2-Personal
    Encryption              : CCMP
    BSSID 1                 : 90:ab:82:ab:cd:ab
         Signal             : 30%
         Radio type         : 802.11n
         Channel            : 1
         Basic rates (Mbps) : 1 2 5.5 11
         Other rates (Mbps) : 6 9 12 18 24 36 48 54

SSID 10 : SSID number 10
    Network type            : Infrastructure
    Authentication          : WPA2-Personal
    Encryption              : CCMP
    BSSID 1                 : 14:ab:82:ab:27:ab
         Signal             : 70%
         Radio type         : 802.11ac
         Channel            : 1
         Basic rates (Mbps) : 1 2 5.5 11
         Other rates (Mbps) : 6 9 12 18 24 36 48 54"""


def get_netsh_fake_data_short(*args, **kwargs):
    return b"""
Interface name : Wi-Fi 
There are 1 networks currently visible. 

SSID 1 : SSID1 Name
    Network type            : Infrastructure
    Authentication          : WPA2-Personal
    Encryption              : CCMP 
"""


def get_netsh_interface_down(*args, **kwargs):
    return b"""
Interface name : Wi-Fi
The wireless local area network interface is powered down and doesn't support the requested operation.
"""

def get_fake_mac(*args, **kwargs):
    return 'aa:bb:cc:dd:ee:ff'

def get_fake_getmac_v(*args, **kwargs):
    return b"""
Connection Name Network Adapter Physical Address    Transport Name
=============== =============== =================== ==========================================================
Wi-Fi           Dell Wireless 1 AA-BB-CC-DD-EE-FF   \Device\Tcpip_{DCA87622-B097-46B0-9F57-B215C80FD15B}
Bluetooth Netwo Bluetooth Devic FF-EE-DD-CC-BB-AA   Media disconnected
"""

class Test(object):

    @mock.patch('pylates.platform_network_managers.WindowsNetworkManager.get_interface_mac_address',
                side_effect=get_fake_mac)
    def setup(self, get_mac_fake):
        self.wnm = WindowsNetworkManager()

    @mock.patch('subprocess.check_output', side_effect=get_netsh_fake_data_long)
    def test_windows_manager_convert_netsh_many(self, get_netsh_fake):
        """Ensure ["netsh", "wlan", "show", "network", "mode=bssid"] converts."""
        points_data = self.wnm.gather_networks_info(self.wnm.CMD_NETSH)
        assert len(points_data) == 10
        assert 'ssid' in points_data[0]
        assert 'bssid' in points_data[0]
        assert type(points_data[0]['bssid']) == list
        assert len(points_data[0]['bssid']) == 2
        assert 'network_type' in points_data[0]
        assert 'authentication' in points_data[0]
        assert 'encryption' in points_data[0]


    @mock.patch('subprocess.check_output', side_effect=get_netsh_fake_data_short)
    def test_windows_manager_convert_netsh_single(self, get_netsh_fake):
        """Ensure ["netsh", "wlan", "show", "network", "mode=bssid"] converts."""
        points_data = self.wnm.gather_networks_info(self.wnm.CMD_NETSH)
        assert len(points_data) == 1


    @mock.patch('subprocess.check_output', side_effect=get_netsh_interface_down)
    def test_windows_manager_convert_netsh_interface_down(self, get_netsh_fake):
        """Ensure ["netsh", "wlan", "show", "network", "mode=bssid"] converts."""
        points_data = self.wnm.gather_networks_info(self.wnm.CMD_NETSH)
        assert len(points_data) == 0

    @mock.patch('subprocess.check_output', side_effect=get_fake_getmac_v)
    def test_get_interface_mac(self, get_getmac_v_fake):
        mac = self.wnm.get_interface_mac_address()
        assert mac == 'AA-BB-CC-DD-EE-FF'