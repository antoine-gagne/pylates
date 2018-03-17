import argparse
import time

from pylates.ssid_data_point import SSIDDataPoint
from pylates.platform_network_managers import WindowsNetworkManager


class LocalisedWLAN(object):
    def __init__(self, measurer_mac_address, measurer_location, timestamp,
                 wlan_data, **kwargs):
        """Create a localised data point."""
        self.measurer_mac_address = measurer_mac_address
        self.measurer_location = measurer_location
        self.timestamp = timestamp

        self.wlan = wlan_data


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Read command line args')
    parser.add_argument('nb_pts', metavar='nb', type=int,
                        help='Number of data samples to collect.')
    args = parser.parse_args()
    wnm = WindowsNetworkManager()
    localized_points = []
    for i in range(0, args.nb_pts):
        x = input('Input X')
        y = input('Input Y')
        timestamp = time.time()
        points_data = wnm.gather_networks_info(wnm.CMD_NETSH)
        for point in points_data:
            ssid_data_point = SSIDDataPoint(**point)
            localized_points.append(LocalisedWLAN(
                wnm.mac_address, (x, y), timestamp, ssid_data_point))
    a=5
