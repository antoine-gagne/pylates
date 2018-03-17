"""Class file which describes a network information data point collected."""

from pylates import utils


class SSIDDataPoint(object):
    def __init__(self, **kwargs):
        """Initializes a network SSID data point."""
        self.ssid = kwargs.pop('ssid', '')
        self.network_type = kwargs.pop('network_type', '')
        self.authentication = kwargs.pop('authentication', '')
        self.encryption = kwargs.pop('encryption', '')
        self.bssid = []
        for bssid_dict in kwargs.pop('bssid', []):
            self.bssid.append(BSSIDData(**bssid_dict))


class BSSIDData(object):
    def __init__(self, **kwargs):
        """Initializes a network BSSID data point."""
        self.name = kwargs.get('name', '')
        self.signal_quality = kwargs.get('signal', '')
        self.radio_type = kwargs.get('radio_type', '')
        self.channel = kwargs.get('signal', '')
        self.basic_rates = kwargs.get('basic_rates', [])
        self.other_rates = kwargs.get('other_rates', [])

    @property
    def signal_rssi(self):
        """RSSI in DB is clamped between -50 and -100 DB."""
        return max(min(self.signal_quality / 2 - 100, -50), -100)

    @property
    def mac_address(self):
        """Find the mac address in the name, if available."""
        return utils.find_mac_address(self.name)
