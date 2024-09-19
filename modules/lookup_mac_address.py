from requests import get
import re
from .list_mac_addresses import ListMacAddresses

class LookupMacAddresses(ListMacAddresses):
    """
    Class to look up MAC addresses from results of nmap scan and match them to their respective vendors.
    """

    def __init__(self, folder):
        """
        Constructor method
        """
        super().__init__(folder)

    def lookup_mac_address(self):
        """
        Method to extract and list MAC addresses from scan results and then look up their respective vendors.
        """
        self.list_mac_addresses()
        print('Looking up MAC addresses to find vendors...')
        mac_list = open(f'{self.folder}Details/mac_addresses.txt', 'r')
        line_by_line = mac_list.readlines()
        with open(f'{self.folder}Details/vendors.txt', 'w') as vendors:
            for i in line_by_line:
                lookup = f'https://macvendors.co/api/{i.strip()}/xml'
                output = get(lookup).text
                find_detail = re.search(pattern=f".*(<company>)(.*)(</company>)", string=output)
                if find_detail:
                    with open(f'{self.folder}Details/vendors.txt', 'a') as vendors:
                        vendors.write('The MAC address: ' + i.strip() + ' belongs to ' + find_detail.group(2) + '\n')
                else:
                    with open(f'{self.folder}Details/vendors.txt', 'a') as vendors:
                        vendors.write('The MAC address: ' + i.strip() + ' has an unknown company association, '
                                                                'it may be wise to check further details related to '
                                                                'this device to ensure it is secure. \n')
