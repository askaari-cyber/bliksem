import requests

class GatherExternal:
    """Class to gather external IP address using an external service"""

    def __init__(self, url: str = 'https://api.ipify.org'):
        """Initialize the ExternalIPGatherer

        Args:
            url (str, optional): The URL of the external service to use. Defaults to 'https://api.ipify.org'.
        """
        self.url = url

    def gather_external(self):
        """Gather the external IP address using the external service
        """
        try:
            # Get the external IP address using an external service
            external_ip = requests.get(self.url).text
            return external_ip
        except Exception as e:
            print(f"Failed to gather external IP: {e}")
            return None
