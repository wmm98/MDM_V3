from Common.process_shell import Shell
from Common.public_page import PublicPage
shell = Shell()


class DevicePage(PublicPage):
    def __init__(self, device_name):
        self.device_name = device_name

    def send_adb_shell_command(self, cmd):
        cmd = "adb -s %s shell %s" % (self.device_name, cmd)
        return shell.invoke(cmd)

    def get_device_serial(self):
        cmd = "getprop ro.serialno"
        return self.send_adb_shell_command(cmd)

