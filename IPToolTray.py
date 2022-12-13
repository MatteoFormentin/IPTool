import pystray
from PIL import Image
import ctypes
import os
import sys

from IPToolCore import IPToolCore

class IPToolTray:

    def __init__(self) -> None:

        self.core = IPToolCore()
        self.first_update = True

        if not self.core.isAdmin():
            ctypes.windll.user32.MessageBoxW(0, "IPTool requires administrative privileges", "Error", 0x10)
            sys.exit(0)

        base_path = getattr(sys, '_MEIPASS', os.path.dirname(
            os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "icon.ico")

        self.icon = pystray.Icon(
            "IPTool",
            icon=Image.open(icon_path),
            menu=pystray.Menu(lambda : (self.getMenu()))
        )

    def run(self):
        self.icon.run()
    
    def getMenu(self):
        try:
            self.core.loadConfigurations()
        except Exception as e:
            if self.first_update:
                ctypes.windll.user32.MessageBoxW(0, "Error in the configuration file!", "Error", 0x10)
            else:
                self.icon.notify("Error in the configuration file!")

        self.core.loadInterfaces()

        menu_items = []
        for curr_iface_name in self.core.ifaces:
            menu_items.append(
                pystray.MenuItem(
                    curr_iface_name,
                    pystray.Menu(
                        *self.getIfacesMenuItems(curr_iface_name))
                )
            )

        menu_items.append(pystray.Menu.SEPARATOR)
        
        menu_items.append(
            pystray.MenuItem(
                "Reload Config",
                lambda: (
                    self.icon.update_menu()
                )
            )
        )

        menu_items.append(
            pystray.MenuItem(
                "Exit",
                lambda: (
                    self.quit()
                )
            )
        )

        self.first_update = False
        return menu_items


    def getIfacesMenuItems(self, iface_name):
        ifaces_menu_items = []
        ifaces_menu_items.append(pystray.MenuItem("Auto - DHCP", lambda icon, item: self.onClick(iface_name, "DHCP")))
        ifaces_menu_items.append(pystray.Menu.SEPARATOR)
        for c in self.core.configurations:
            ifaces_menu_items.append(pystray.MenuItem(
                c.name, lambda icon, item: self.onClick(iface_name, item.text)))
        return ifaces_menu_items
    
    def onClick(self, iface_name, conf_name):
        print(str(iface_name) + ":" + str(conf_name))
        if conf_name == "DHCP":
            res = self.core.setDhcp(iface_name)
        else:
            res = self.core.setStaticIP(iface_name, self.core.getConfigurationFromName(conf_name))
        
        if res:
            self.icon.notify("IP Configuration for {0} set to {1}".format(iface_name, conf_name))
        else:
            self.icon.notify("Configuration already applied!")

    def quit(self):
        self.icon.visible = False
        self.icon.stop()    
