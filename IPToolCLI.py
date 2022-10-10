from time import sleep
from sys import exit

from IPToolCore import IPToolCore

class IPToolCLI:
    def __init__(self) -> None:
        self.core = IPToolCore()

    def run(self):
        print("IPTool v1.0")

        if not self.core.isAdmin():
            print("ERROR: You must run this as administrator!")
            input("Press enter to exit.")
            exit(0)

        try:
            self.core.loadConfigurations()
        except Exception as e:
            print("ERROR: Invalid configurations file!")
            input("Press enter to exit.")
            exit(0)

        if len(self.core.configurations) == 0:
            print("ERROR: No valid configurations found!")
            input("Press enter to exit.")
            exit(0)

        self.core.loadInterfaces()
        if len(self.core.ifaces) == 0:
            print("ERROR: No interfaces found!")
            input("Press enter to exit.")
            exit(0)

        self.printIfaces()
        valid_in = False
        iface_selection = 0
        while not valid_in:
            s = input(
                "Choose an interface (0 - {0}): ".format(len(self.core.ifaces) - 1))
            if s.isdigit():
                iface_selection = int(s)
                if 0 <= iface_selection < len(self.core.ifaces):
                    valid_in = True
            if not valid_in:
                print("Invalid selection, retry!")

        self.printConfigurations()
        valid_in = False
        selection = 0
        while not valid_in:
            s = input(
                "Choose an IP configuration to apply (0 - {0}): ".format(len(self.core.configurations)))
            if s.isdigit():
                selection = int(s)
                if 0 <= selection <= len(self.core.configurations):
                    valid_in = True
            if not valid_in:
                print("Invalid selection, retry!")

        if selection == 0:
            res = self.core.setDhcp(self.core.ifaces[iface_selection])
        else:
            res = self.core.setStaticIP(self.core.ifaces[iface_selection], self.core.configurations[selection - 1])

        if res:
            print("Done!")
        else:
            print("Error! Please check the configuration")

        sleep(1)

    def printConfigurations(self):
        print("\n\nAvailable configurations:")
        print("0 - DHCP\n")
        for i in range(len(self.core.configurations)):
            c = self.core.configurations[i]
            print("{0} - {1}".format(i + 1, c.name))
            print("IP:   {0}".format(c.static_ip))
            print("Mask: {0}".format(c.subnet_mask))
            print("GW:   {0}".format(c.default_gw))
            print()

    def printIfaces(self):
        print("Available Interfaces:")
        for i in range(len(self.core.ifaces)):
            print("{0} - {1}".format(i, self.core.ifaces[i]))
