# import all necessary modules for the project
import optparse
from requests import get
import requests
import pyfiglet
from shodan import Shodan, APIError
import datetime
from modules.__init__ import *

# Parser allows for user input by using an option key to input a value, in this case a Shodan API key
parser = optparse.OptionParser()
parser.add_option("--api", "-a", dest="api_key", help="API key for Shodan")
(options, arguments) = parser.parse_args()
api_key = options.api_key


# Prints a banner to the terminal to indicate that the program is running.
def header():
    ascii_banner = pyfiglet.figlet_format("Bliksem Smart Home Scanner!", font='smslant')
    return ascii_banner

def end():
    return pyfiglet.figlet_format("Thanks for using Askaari's Home Scanner!", font='smslant')
    

# Main function runs all the sub functions in specific order
def main():
    print(header())
    # Creating a folder structure using the days date in order to help the user keep track of their scans.
    date = datetime.datetime.now().date()
    now = str(date)
    folder = './Scan_results_' + now + '/'
    Creation.make_dir()

    ip = FindIP.ip()
    find_subnet = FindSubnet(ip)
    subnet = find_subnet.subnet()

    # Calls the external nmap function
    external_nmap = ExternalNmap(api_key, folder)
    external_nmap.scan()

    creds_checker = CheckCreds(ip, folder)
    creds = creds_checker.default_creds_check()

    internal_nmap = InternalNmap(folder, subnet, creds)
    internal_nmap.internal_nmap()

    lookup_mac_address = LookupMacAddresses(folder)
    lookup_mac_address.lookup_mac_address()

    shodan = ShodanCheck(api_key, folder)
    shodan.check()

    print(end())


# Calls main function in order to start program
if __name__ == '__main__':
    try:
        main()
    # If user interrupts script with keyboard, exception will be processed and program will be stopped.
    except KeyboardInterrupt:
        print("\nKeyboard has interrupted")
        print("Stopping program...")

