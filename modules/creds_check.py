import socket
from telnetlib import Telnet

class CheckCreds:
    def __init__(self, host, folder):
        self.host = host
        self.folder = folder

    def default_creds_check(self):
        global test
        creds = ['root:1111', 'root:1234', 'root:12345', 'root:123456', 'root:54321', 'root:666666', 'root:7ujMko0admin',
                 'root:7ujMko0vizxv', 'root:888888', 'root:admin', 'root:anko', 'root:default', 'root:dreambox',
                 'root:hi3518', 'root:ikwb', 'root:juantech', 'root:jvbzd', 'root:klv123', 'root:klv1234', 'root:pass',
                 'root:password', 'root:realtek', 'root:root', 'root:system', 'root:user', 'root:vizxv', 'root:xc3511',
                 'root:xmhdipc', 'root:zlxx.', 'root:Zte521', '666666:666666', '888888:888888', 'admin:1111',
                 'admin:1111111', 'admin:1234', 'admin:12345', 'admin:123456', 'admin:54321', 'admin:7ujMko0admin',
                 'admin:admin', 'admin:admin1234', 'admin:meinsm', 'admin:pass', 'admin:password', 'admin:smcadmin',
                 'admin1:password', 'administrator:1234', 'Administrator:admin', 'guest:12345', 'guest:guest',
                 'root:0', 'service:service', 'supervisor:supervisor', 'support:support', 'tech:tech',
                 'ubnt:ubnt', 'user:user']

        open(f'{self.folder}Brute_force/telnet_result.txt', 'w')
        for cred in creds:
            user = cred.split(":")[0]
            passwd = cred.split(":")[1]
            try:
                test = CheckCreds.access(user, passwd, self.host)
                with open(f'{self.folder}Brute_force/telnet_result.txt', 'a') as tntxt:
                    tntxt.write('Host ' + self.host + ' has been successfully compromised using the username `'
                                + user + '` and the password `' + passwd + '`, meaning it is vulnerable to brute force attack.\n\n')

                with open(f'{self.folder}Key_findings/Summary.txt', 'a+') as summtxt:
                    summtxt.write(
                        '\nBRUTE FORCE:\n' + 'Host ' + self.host + ' has been successfully compromised using the username/password combination `'
                        + user + ':' + passwd + '`, meaning it is vulnerable to brute force attack.\nRecommendation: '
                                                'Change the password for the host above, do not use any default passwords.\n')
                return test
            except socket.timeout:
                continue

    # Function used to run telnet using username, password and host values retrieved from default_creds_check function.
    @staticmethod
    def access(user, password, host):
        passwd_check = Telnet(host, 23, 0.5)
        passwd_check.read_until(b'login: ', 0.5)
        passwd_check.write(user.encode('ascii') + b'\n')
        if password:
            passwd_check.read_until(b'Password: ', 0.5)
            passwd_check.write(password.encode('ascii') + b'\n')
        passwd_check.write(b'ls\n')
        passwd_check.write(b'exit\n')
        result = passwd_check.read_all().decode('ascii')
        passwd_check.close()
        return result
