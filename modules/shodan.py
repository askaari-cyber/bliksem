from modules.gather_external import GatherExternal
from shodan import Shodan, APIError

class ShodanCheck:
    """
    Class to search Shodan online for external IP address in order to reveal any potential public information.
    """

    def __init__(self, api_key, folder):
        """
        Initialize the ShodanCheck class

        Parameters:
            api_key (str): The Shodan API key
            folder (str): The folder to write the results to
        """
        self.api_key = api_key
        self.folder = folder

    def check(self):
        """
        Search Shodan online for external IP address in order to reveal any potential public information.
        """
        gatherer = GatherExternal()
        external_ip = gatherer.gather_external()
        if not self.api_key:
            print("No Shodan API key, bypassing this check")
            return

        try:
            lookup = Shodan(self.api_key)
            info = lookup.host(external_ip)
            with open(f'{self.folder}Details/shodan_info.txt', 'w') as shodantxt:
                shodantxt.write("IP: {}, Company: {}, Operating System: {}\n".format(
                    info['ip_str'], info.get('org'), info.get('os')))
                for port in info['data']:
                    shodantxt.write("Port: {}, Banner: {}\n".format(port['port'], port['data']))
        except APIError as e:
            print(f"An error occurred with the Shodan API: {e}")

