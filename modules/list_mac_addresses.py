import re

class ListMacAddresses:
    """
    Class to handle extracting and listing MAC addresses from scan results.
    """
    def __init__(self, folder):
        """
        Constructor for ListMacAddresses class.

        :param folder: A string representing the full path to the folder containing the scan results.
        """
        self.folder = folder

    def list_mac_addresses(self):
        """
        Method to extract and list MAC addresses from scan results.
        """
        print('Extracting MAC Addresses from scan results...')
        with open(f"{self.folder}Nmap/internal_nmap.nmap") as file:
            mac_addresses = [line.split('MAC Address: ')[1].strip() for line in file if 'MAC Address: ' in line]
        with open(f'{self.folder}Details/mac_addresses.txt', 'w') as macs:
            macs.write('\n'.join(mac_addresses))
