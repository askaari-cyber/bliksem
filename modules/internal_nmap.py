import nmap
import re
from requests import get

class InternalNmap:
    def __init__(self, folder, subnet, creds):
        self.folder = folder
        self.subnet = subnet
        self.creds = creds


    def internal_nmap(self):
        print('Performing internal port scanning of subnet...')
        nm = nmap.PortScanner()
        scan_args = [
            '-sS',  # TCP SYN scan
            '-sC',  # Scan for common services
            '-Pn',  # No ping, just scan
            '-n',   # No DNS resolution
            '-O',   # OS detection
            '-p1-1024,2424,8080,8443,5000,8081,3389,48101',  # Ports to scan
            '--open',  # Only show open ports
            '-oN', f'{self.folder}Nmap/internal_nmap.nmap'
        ]

        nm.scan(hosts=self.subnet, arguments=' '.join(scan_args))
        open_ports = set()
        for host in nm.all_hosts():
            if 'tcp' in nm[host]:
                open_ports.update(nm[host]['tcp'].keys())

        with open(f'{self.folder}Details/services.txt', 'w') as servicestxt:
            for host in nm.all_hosts():
                if 'tcp' in nm[host]:
                    host_ports = set(nm[host]['tcp'].keys())
                    servicestxt.write(
                        '\nHost: ' + host + ' has the following open ports:\n' + ', '.join(map(str, host_ports)) + '\n')
        for port in open_ports:
            if port == 23:
                self.creds
                mac = nm[host]['addresses']['mac']
                if mac:
                    lookup = f'https://macvendors.co/api/{mac}/xml'
                    output = get(lookup).text
                    vendor = re.search(r".*<company>(.*)</company>", output)

                    if vendor:
                        vendor_name = vendor.group(1)
                    else:
                        vendor_name = 'Unknown'

                    with open(f'{self.folder}Brute_force/telnet_result.txt', 'a') as tntxt:
                        tntxt.write(f'The device with MAC address of {mac} has port 23 open, the telnet service is '
                                    f'often used by hackers to brute force devices. It is recommended to close this '
                                    f'port, or if port is required ensure a strong password is set. \n'
                                    f'This device comes from {vendor_name}. If this is an unknown or potentially '
                                    f'suspicious vendor, check online to ensure there are no vulnerabilities '
                                    f'associated with the device.\n')
            if port in nm[host]['tcp']:
                details = nm[host]['tcp'][port]
                service_name = details['name']
                with open(f'{self.folder}Details/services.txt', 'a') as servicestxt:
                    if 'unknown' in service_name.lower():
                        servicestxt.write(f'Port {port} is running an unknown service\n')
                    else:
                        servicestxt.write(f'Port {port} is running {service_name}\n')
                if service_name.lower() in ['ssh', 'telnet'] or port in [23, 2323]:
                    with open(f'{self.folder}Key_findings/Summary.txt', 'a') as summtxt:
                        summtxt.write('\nInternal finding:\nThe host '
                                    + host + ' has port ' + str(port)
                                    + ' open. Telnet and SSH are common targets for brute force attacks. Botnets such'
                                        ' as Mirai use telnet to exploit and increase their collection of devices.'
                                        '\nRecommendation: Ensure a strong password is used to access the device on '
                                        'this port and do not allow guest access to the device.\n')
                if port == 3389:
                    with open(f'{self.folder}Key_findings/Summary.txt', 'a') as summtxt:
                        summtxt.write('\nInternal finding:\nThe host '
                                    + host + ' has port ' + str(port)
                                    + ' open. The RDP service runs on this port and has the potential to allow an '
                                        'attacker full access to the device.\nRecommendation: If this host has a strong '
                                        'password then this is a minimal threat, however, if a common or weak password '
                                        'is used, it should be changed as soon as possible.\n')
                if port in [445, 139]:
                    with open(f'{self.folder}Key_findings/Summary.txt', 'a') as summtxt:
                        summtxt.write('\nInternal finding:\nThe host '
                                    + host + ' has port ' + str(port)
                                    + ' open. Ports 445 and 139 are used for SMB share drives and if not configured '
                                        'properly, could make sensitive information available to unwanted users. '
                                        'Additionally, if network shares allow guest access or access using weak '
                                        'credentials, any files stored on this share drive could be read or downloaded '
                                        'by an attacker.\nRecommendation: Ensure any network shares are only accessible '
                                        'to those who require access and that the accounts with access have strong '
                                        'passwords set to avoid sensitive information being leaked.\n')
                if port == 48101:
                    with open(f'{self.folder}Key_findings/Summary.txt', 'a') as summtxt:
                        summtxt.write('\nInternal finding:\nThe host '
                                    + host + ' has port ' + str(port)
                                    + ' open. As reported by the CISA, this port is often used by malicious actors in'
                                        ' order to spread malware. As a result this port is unusual to have open and '
                                        'could indicate a compromised device.\nRecommendation: If the device is not '
                                        'necessary, unplug it. If it is necessary, access the application or UI which '
                                        'controls the device and check if it is possible to close the port. If this is '
                                        'not possible check on the manufacturers website or contact them for assistance '
                                        'in closing the port. Additionally, check the full nmap scan result for this '
                                        'host in order to assess if any other malicious services are open.\n')
                if port == 80:
                    with open(f'{self.folder}Key_findings/Summary.txt', 'a') as summtxt:
                        summtxt.write('\nInternal finding:\nThe host '
                                    + host + ' uses HTTP to host a web service. HTTP is an insecure service which'
                                            ' permits unencrypted communication. The service being hosted can be'
                                            ' found by visiting http://' + host
                                    + '. If this is a login portal for a router, there is great risk associated with '
                                        'having this port open, attackers can intercept any login attempts and can use '
                                        'the open port to ultimately gain control of the device by intercepting the login '
                                        'credentials.\nRecommendation: It is highly recommended to only use services '
                                        'which enforce SSL/TLS in order to prevent Man-In-The-Middle and sniffing '
                                        'attacks. As a result it is recommended to update the device to the latest '
                                        'version, access the device settings to run on a HTTPS web service, enforcing '
                                        'SSL/TLS. Additionally, if possible, close the port.\n')
        return nm



