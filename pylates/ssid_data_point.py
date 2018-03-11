"""Class file which describes a network information data point collected."""

import time

from pylates import utils


class SSIDDataPoint(object):
    def __init__(self, measurer_mac_address='', measurer_location=None,
                 **kwargs):
        """Initializes a network SSID data point."""
        self.measurer_mac_address = measurer_mac_address
        self.measurer_location = measurer_location
        self.timestamp = kwargs.pop('timestamp', time.time())

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
