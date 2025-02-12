import os.path
import time
from datetime import datetime

from Common.process_shell import Shell
from Common.public_page import PublicPage
from Common.log import MyLog
shell = Shell()
log = MyLog()


class DevicePage(PublicPage):
    def __init__(self, device_name):
        self.device_name = device_name

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
        result = self.remove_special_char(self.send_adb_shell_command("\"md5sum %s | awk {'print $1'}\"" % file_path))
        print("result:", result)
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

    def is_screen_on(self):
        res = self.send_adb_shell_command("\"dumpsys window | grep mAwake\"")
        if "mAwake=true".upper() in self.remove_special_char(res).upper():
            return True
        else:
            return False

    def press_power_button(self):
        self.send_adb_shell_command("input keyevent KEYCODE_POWER")

    def back_home(self):
        self.send_adb_shell_command("input keyevent KEYCODE_BACK")

    def unlock(self):
        self.send_adb_shell_command("input swipe 300 500 300 0")

    def ping_network(self, times=5, timeout=300):
        # 判断设备是否可上网
        # 每隔0.6秒ping一次，一共ping5次
        # ping - c 5 - i 0.6 qq.com
        log.info("检查设备网络")
        now_time = self.get_current_time()
        while True:
            log.info("正在 ping www.baidu.com.. ")
            if self.is_network(times=5):
                log.info("ping www.baidu.com 成功")
                return True
            if self.get_current_time() > now_time + timeout:
                log.error("ping www.baidu.com失败 请检测！！！")
                return False
            time.sleep(3)

    def is_network(self, times=5):
        cmd = "ping -c %s %s" % (times, "www.baidu.com")
        exp = self.remove_special_char("ping: unknown host %s" % "www.baidu.com")
        res = self.send_adb_shell_command(cmd)
        if res:
            res1 = self.remove_special_char(res)
            if exp in res1 or len(res1) == 0:
                return False
            else:
                return True
        else:
            return False

    def enable_wifi_btn(self):
        self.send_adb_shell_command("svc wifi enable")

    def disable_wifi_btn(self):
        self.send_adb_shell_command("svc wifi disable")

    def get_wifi_btn_status(self):
        return self.send_adb_shell_command("settings get global wifi_on")

    def wifi_is_enable(self):
        if "1" in self.get_wifi_btn_status():
            return True
        else:
            return False





