"""Allows user to collect data in a consistent manner."""

import re
import subprocess


class PlatformNetworkManager(object):
    """Base class for platforms to implement.

    These classes implement methods to interact with the network and
    collect data.
    """

    def __init__(self):
        pass

    def gather_networks_info(self, method):
        pass


class WindowsNetworkManager(PlatformNetworkManager):
    """Implement the Windows platform interaction with the network."""

    CMD_NETSH = ["netsh", "wlan", "show", "network", "mode=bssid"]

    def __init__(self):
        super(WindowsNetworkManager).__init__()

    def gather_networks_info(self, method):
        # Switch cmd below to change how data is collected
        network_list_raw = self._execute_gather_method(method)
        points_data = self._convert_command_output_to_dicts(
            method, network_list_raw)
        return points_data

    def _execute_gather_method(self, method):
        """Use a specific method to gather data regarding the networks."""
        if method == self.CMD_NETSH:
            return subprocess.check_output(method)

    def _convert_command_output_to_dicts(self, cmd, netsh_output):
        """Convert the 'netsh wlan show network "mode=bssid" output to dicts."""
        lines = netsh_output.splitlines()
        ssid_dicts = []
        if cmd == self.CMD_NETSH:
            ssid_reg = re.compile(r'^SSID \d* :.*$')
            ssid_locs = []
            ssid_infos = []
            for line_no in range(0, len(lines)):
                if ssid_reg.match(lines[line_no]):
                    ssid_locs.append(line_no)
                    if len(ssid_locs) > 1:
                        ssid_infos.append(lines[ssid_locs[-2]:ssid_locs[-1]])
            for ssid_info in ssid_infos:
                ssid_dict = {'bssid': []}
                for line in ssid_info:
                    if not line:
                        break
                    k, v = line.split(':', 1)
                    k = k.strip()
                    v = v.strip()
                    if re.match(r'SSID \d+', k):
                        ssid_dict['ssid'] = v
                    elif k == 'Network type':
                        ssid_dict['network_type'] = v
                    elif k == 'Authentication':
                        ssid_dict['authentication'] = v
                    elif k == 'Encryption':
                        ssid_dict['encryption'] = v
                    elif re.match(r'BSSID \d+', k):
                        ssid_dict['bssid'].append({'name': v})
                    elif k == 'Signal':
                        v = int(v.replace('%', ''))
                        ssid_dict['bssid'][-1]['signal'] = v
                    elif k == 'Radio type':
                        ssid_dict['bssid'][-1]['radio_type'] = v
                    elif k == 'Channel':
                        ssid_dict['bssid'][-1]['channel'] = v
                    elif k == 'Basic rates (Mbps)':
                        v = v.split(' ')
                        v = [float(x) for x in v]
                        ssid_dict['bssid'][-1]['basic_rates'] = v
                    elif k == 'Other rates (Mbps)':
                        v = v.split(' ')
                        v = [float(x) for x in v]
                        ssid_dict['bssid'][-1]['other_rates'] = v
                ssid_dicts.append(ssid_dict)
            return ssid_dicts
