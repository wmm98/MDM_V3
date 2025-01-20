import os.path
import time
from datetime import datetime

from Common.process_shell import Shell
from Common.public_page import PublicPage
shell = Shell()


class DevicePage(PublicPage):
    def __init__(self, device_name):
        self.device_name = device_name

    def time_to_timestamp(self, time_str):
        time_format = "%Y-%m-%d %H:%M:%S"
        dt_object = datetime.strptime(time_str, time_format)
        timestamp = int(dt_object.timestamp())
        return timestamp

    # 获取当前的时间戳，精确到s
    def get_current_timestamp(self):
        return int(time.time())

    def send_adb_shell_command(self, cmd):
        cmd = "adb -s %s shell %s" % (self.device_name, cmd)
        return shell.invoke(cmd)

    def get_device_serial(self):
        cmd = "getprop ro.serialno"
        return self.send_adb_shell_command(cmd)

    def remove_file(self, file_path):
        cmd = "rm -rf %s" % file_path
        if self.file_is_exist(file_path):
            self.send_adb_shell_command(cmd)

    def file_is_exist(self, file_path):
        cmd = "ls %s" % file_path
        result = self.send_adb_shell_command(cmd)
        if result.find(os.path.basename(file_path)) != -1:
            return True
        else:
            return False

    def remove_dir(self, dir_path):
        cmd = "rm -rf %s" % dir_path
        self.send_adb_shell_command(cmd)

    def push_file(self, local_file_path, remote_file_path):
        cmd = "push %s %s" % (local_file_path, remote_file_path)
        return self.send_adb_shell_command(cmd)

    def pull_file(self, remote_file_path, local_file_path):
        cmd = "pull %s %s" % (remote_file_path, local_file_path)
        return self.send_adb_shell_command(cmd)

    def get_file_md5(self, file_path):
        cmd = "md5sum %s | awk {'print $1'}" % file_path
        result = self.remove_special_char(self.send_adb_shell_command(cmd))
        return result

    def reboot_device(self):
        cmd = "reboot"
        self.send_adb_shell_command(cmd)

    def device_is_boot(self):
        cmd = "getprop sys.boot_completed"
        result = self.send_adb_shell_command(cmd)
        if result.find("1") != -1:
            return True
        else:
            return False

    def devices_adb_online(self):
        result = self.remove_special_char(shell.invoke("adb devices"))
        if result.find(self.device_name + "device") != -1:
            return True
        else:
            return False

    def restart_adb_server(self):
        shell.invoke("adb kill-server")
        shell.invoke("adb start-server")
        time.sleep(1)



