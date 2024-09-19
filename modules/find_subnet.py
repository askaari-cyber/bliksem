from .find_IP import FindIP
import ipaddress


class FindSubnet:
    def __init__(self, ip):
        self.ip = ip

    def subnet(self):
        subnet = ipaddress.ip_network(self.ip + '/255.255.255.0', strict=False)
        print('Your home subnet is: ' + str(subnet))
        return str(subnet)
