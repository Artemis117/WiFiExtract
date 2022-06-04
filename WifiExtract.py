# import lang
import locale
import subprocess
import platform
import re

import lang


def Os_detect():
    """ Detect OS """
    return platform.system()


def command_execute(cmd):
    """ execute the command and return the output """
    return subprocess.run(cmd, capture_output=True).stdout.decode(errors="ignore")


def get_lang():
    """ detect system language """
    return locale.getdefaultlocale()[0]


class WifiExtract:

    def __init__(self):

        self.save = False
        self.verbose = False
        self.lang_operating = None
        self.list_wifi = list()

        # set the language to use
        self.define_lang()

    def define_lang(self):

        if get_lang() == "fr_FR":

            print('language detect : fr_FR')
            self.lang_operating = lang.fr_FR
        else:
            print('Default language : ENG')
            pass

    def save_wifi(self, save):
        self.save = save

    def write_file(self):
        """ write SSID and find passwords to a file """
        name_file = platform.node() + ".txt"
        file = open(name_file, "w")

        for ssid in self.list_wifi:
            line = f"SSID : {ssid['SSID']} ; Password : {ssid['Password']}"
            file.write(line + '\n')

        file.close()

    def extract_windows_Wifi(self, save=False, verbose=False):

        self.save = save
        self.verbose = verbose

        profile_name = command_execute(["netsh", "wlan", "show", "profiles"])
        profile_name = re.findall(self.lang_operating["profiles"], profile_name)

        if len(profile_name) == 0:
            print("No Wi-Fi found in the system.")

        else:
            for name in profile_name:

                profile = dict()

                profile_info = command_execute(["netsh", "wlan", "show", "profile", name])
                if re.search(self.lang_operating["key_present"], profile_info):
                    continue
                else:
                    profile["SSID"] = name
                    profile_info_password = command_execute(["netsh", "wlan", "show", "profile", name, "key=clear"])
                    password = re.search(self.lang_operating["key"], profile_info_password)

                    if password is None:
                        profile["Password"] = None
                    else:
                        profile["Password"] = password[1]

                    # Show SSID and Password Found
                    if self.verbose:
                        print(profile)

                # Adding Wi-Fi to the list
                self.list_wifi.append(profile)

        # Save the Wi-Fi list
        if self.save:
            self.write_file()

    def extract_linux_Wifi(self, save=False, verbose=False):
        pass

    def extract_mac_Wifi(self, save=False, verbose=False):
        pass
