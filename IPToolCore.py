import ctypes
import xml.etree.ElementTree as ET
import subprocess


SHOW_IFACE_COMMAND = "netsh interface show interface"
SET_DHCP_IP_COMMAND = """netsh interface ip set address name = "{0}" dhcp"""
SET_STATIC_IP_COMMAND = """netsh interface ip set address name = "{0}" static {1} {2} {3}"""

class Configuration:
    def __init__(self, _name:str, _static_ip:str, subnet_mask:str, _default_gw:str="" ) -> None:
        self.name = _name
        self.static_ip = _static_ip
        self.subnet_mask = subnet_mask
        self.default_gw = _default_gw


class IPToolCore:

    def __init__(self, _config_path="configurations.xml") -> None:
        self.config_path = _config_path
        self.configurations = []
        self.ifaces = []

    def loadInterfaces(self):
        self.ifaces = []
        iface_str = subprocess.check_output(SHOW_IFACE_COMMAND).splitlines()[3:-1]
        for s in iface_str:
            iface = str(s).split("  ")[-1:][0].strip('\'')
            self.ifaces.append(iface)

    def loadConfigurations(self):
        self.configurations = []
        tree = ET.parse(self.config_path)
        root = tree.getroot()
        for conf in root.iter("configuration"):
            name = conf.get("name")
            static_ip = conf.find("ip")
            subnet_mask = conf.find("mask")
            default_gw = conf.find("gw")
            if static_ip != None:
                static_ip = static_ip.text
                subnet_mask = subnet_mask.text
                default_gw = default_gw.text
                if default_gw == None:
                    default_gw = ""
            else:
                static_ip = ""
                subnet_mask = ""
                default_gw = ""

            c = Configuration(name, static_ip, subnet_mask, default_gw)

            self.configurations.append(c)
    
    def setDhcp(self, iface_name):
        command = SET_DHCP_IP_COMMAND.format(iface_name)
        try:
            subprocess.check_output(command, shell=True)
            return True
        except subprocess.CalledProcessError as grepexc:
            return False

    def setStaticIP(self, iface_name, configuration):
        command = SET_STATIC_IP_COMMAND.format(iface_name, configuration.static_ip, configuration.subnet_mask, configuration.default_gw)
        try:
            subprocess.check_output(command, shell=True)
            return True
        except subprocess.CalledProcessError as grepexc:   
            return False
    
    def getConfigurationFromName(self, conf_name):
        for c in self.configurations:
            if c.name == conf_name:
                return c
        return None

    def isAdmin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False