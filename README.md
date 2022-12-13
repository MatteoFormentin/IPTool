# IPTool
Simple tool to manage multiple IP configuration directly from tray bar: right click on tray icon, choose the interface and the configuration to apply. 

## How to install
Download the folder from release page, uncompress it in your preferred location.  
Add your ip configuration to a file named configurations.xml, with this sintax:

    <configurations>
      <configuration name="Test1">
        <ip>192.168.139.3</ip>
        <mask>255.255.255.0</mask>
        <gw>192.168.139.1</gw>
      </configuration>
      <configuration name="Test2">
        <ip>192.168.1.7</ip>
        <mask>255.255.255.0</mask>
        <gw>192.168.1.1</gw>
      </configuration>
    </configurations>
## Run at startup
Create a shortcut to IPTool.exe inside  
C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp
