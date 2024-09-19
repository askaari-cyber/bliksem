import nmap
import re
from requests import get
from modules.gather_external import GatherExternal

class ExternalNmap:
    def __init__(self, creds, folder):
        self.creds = creds
        self.folder = folder
        self.nm = nmap.PortScanner()

    def scan(self):
        print('Performing external port scanning...')
        gatherer = GatherExternal()
        external_ip = gatherer.gather_external()

        if not external_ip:
            print("Error: Could not retrieve external IP address.")
            return

        args = f'-sS -Pn -n -p- --open -sC -oN {self.folder}Nmap/external_nmap.nmap'
        ext_scan = self.nm.scan(hosts=external_ip, arguments=args)
        hosts = self.nm.all_hosts()

        for host in hosts:
            ports = list(self.nm[host]['tcp'].keys())
            for port in ports:
                details = self.nm[host]['tcp'][port]
                service_name = f"{details['name']}"
                if service_name.__contains__('http'):
                    self.write_to_summary_file(host, port, service_name)

        # Looks to see if port 23 is open, if it is, then it will run a default credential brute force against
        # the telnet port
        if 23 in [port for host in hosts for port in self.nm[host]['tcp'].keys()]:
            self.creds.default_creds_check(external_ip, self.folder)

        return ext_scan

    def write_to_summary_file(self, host, port, service_name):
        with open(f'{self.folder}Key_findings/Summary.txt', 'a') as summtxt:
            summtxt.write(
                '\nEXTERNAL IP FINDINGS:\nHTTP(s) port ' + str(port)
                + ' is open on your external IP address, this is dangerous as it can grant attackers access to a'
                  ' service running in your home from anywhere in the world. This can be done by finding your '
                  'external IP address and accessing the open web port on any web browser. Often an externally '
                  'open web port can be a router login page, allowing for the potential of credential cracking '
                  'through brute forcing, especially if a weak or default password is in place for the web '
                  'service.\nRecommendation: If the web service is a login portal, ensure an strong password is '
                  'used and any default password is changed. Additionally, if possible, close this port in your '
                  'router settings or set up firewall rules to block access to the port by default.\n')
            if service_name.__contains__('https'):
                summtxt.write('Visit https://' + str(host) + ':' + str(port)
                              + ' on your browser to see the web page - if a login portal is available, login '
                                'and ensure a strong password is set or the service is disabled if not needed.\n')
            else:
                summtxt.write('Visit http://' + str(host) + ':' + str(port)
                              + ' on your browser to see the web page - if a login portal is available, login '
                                'and ensure a strong password is set or the service is disabled if not needed\n')



