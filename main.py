
import getopt
import sys

from IPToolCLI import IPToolCLI
from IPToolTray import IPToolTray

# pyinstaller --windowed --icon="../../icon.ico" --add-binary "../../icon.ico;." --name "IPTool" --specpath "bin/intermediate" --distpath "bin/dist" --workpath="bin/intermediate" "main.py" --exclude-module pywin32-ctypes --exclude-module altgraph --exclude-module pyinstaller-hooks-contrib --exclude-module future --exclude-module pefile --exclude-module pyinstaller --exclude-module libcrypto

def main():
    mode = 1  # 0 cli, 1 tray

    opts, args = getopt.getopt(sys.argv[1:], "c:t:", ['cli', 'tray', ])
    for opt, arg in opts:
        if opt in ('-c', '--cli'):
            mode = 0
        if opt in ('-t', '--tray'):
            mode = 1
        
    if mode == 0:
        iptool = IPToolCLI()
        iptool.run()
    elif mode == 1:
        iptool = IPToolTray()
        iptool.run()


if __name__ == "__main__":
    main()
