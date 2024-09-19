import socket
import re


class FindIP:
    @staticmethod
    def ip():
        host = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        host.connect(("8.8.8.8", 80))   # Connect to google
        # ip = host.getsockname()         # Return IP of the device used to connect to google
        ip = host.getsockname()[0]     # Return the first item (IP address) from the getSockName tuple
        host.close()                   # Always close the socket
        print('Your IP address is: ' + ip)
        # for i in ip:
        #     ip_is = re.match(".*([0-9.]+)", i)  # Regular expression to match IP address
        #     ip = ip_is.group(0)                 # Retrieve just the IP address from the regular expression                      # Convert IP address to string
        #     print('Your IP address is: ' + str(ip))
        return ip                           # Return IP address for use in subnet function
        host.close()
