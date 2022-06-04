import WifiExtract
import sys


app = WifiExtract.WifiExtract()

if WifiExtract.Os_detect() == "Windows":
    print('OS detect : Windows.')
    """ Extract wifi for windows"""
    app.extract_windows_Wifi(verbose=True, save=True)

elif WifiExtract.Os_detect() == "Linux":
    print("OS detect : Linux. \n Not supported")
    sys.exit()
    # TODO : Add wifi extraction for linux

elif WifiExtract.Os_detect() == "Darwin":
    print("OS detect : Mac. \n Not supported")
    sys.exit()
    # TODO : Add Wi-Fi extraction for Mac
else:
    print("System not recognized")
    sys.exit()
