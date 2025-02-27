import os.path
import requests
from datetime import datetime
import hashlib
from PyQt5 import QtWidgets, QtCore
from process_shell import Shell

shell = Shell()


class PostRequestWorker(QtCore.QThread):
    progress = QtCore.pyqtSignal(str)

    def __init__(self, url, data):
        super().__init__()
        self.url = url
        self.data = data

    def run(self):
        response = requests.post(self.url, data=self.data)
        self.progress.emit(response.text)


class public_:
    def __init__(self):
        pass

    def restart_adb(self):
        shell.invoke("adb kill-server")
        shell.invoke("adb start-server")

    def get_devices_list(self):
        devices_info = shell.invoke("adb devices").split("\r\n")[1:-2]
        devices = [device_str.split("\t")[0] for device_str in devices_info if device_str.split("\t")[1] == "device"]
        return devices

    def reboot_device(self, device_name):
        cmd = "reboot"
        return self.send_adb_shell_command(device_name, cmd)

    def send_adb_shell_command(self, device_name, cmd):
        cmd = "adb -s %s shell %s" % (device_name, cmd)
        return shell.invoke(cmd)

    def get_device_serial(self, device_name):
        cmd = "getprop ro.serialno"
        return self.send_adb_shell_command(device_name, cmd)

    def upload_lot(self, info):
        """
        url, file_path, split_file_dir, session_id
        :param info:
        :return:
        """
        responses_list = []
        jason_data = {}
        file_name = os.path.basename(info["file_path"])
        jason_data["file_name"] = file_name
        jason_data["filename"] = file_name
        file_size = os.path.getsize(info["file_path"])
        jason_data["file_size"] = file_size
        jason_data["block_size"] = 10485760
        jason_data["multil_block"] = "true"
        appSecret = "c9537edd37521e415460b45b25a7ffdc"
        file_binaries = []
        jason_data_list = []
        if file_size > 10485760:
            file_parts = self.split_file(info["file_path"], info["file_dir"])
            jason_data['total_blocks'] = len(file_parts)
            time_stamp = str(int(datetime.now().timestamp()))
            token = self.generate_token(appSecret, file_name, time_stamp)
            for i in range(len(file_parts)):
                current_jason_data = jason_data.copy()
                current_jason_data['index'] = i + 1
                current_jason_data['token'] = token
                current_jason_data['timestamp'] = time_stamp
                with open(file_parts[i], 'rb') as file:
                    file = {'data': (file_parts[i], file.read(), 'multipart/form-data')}

                    jason_data_list.append(current_jason_data)
                    file_binaries.append(file)
                    # response = self.m_post(info["url"], session_id=info['session_id'].strip(), files=file, data=jason_data)
                    # print(response.json())
                    # responses_list.append(response.json())
            return jason_data_list, file_binaries
        else:
            jason_data['total_blocks'] = 1
            jason_data['index'] = 1
            time_stamp = str(int(datetime.now().timestamp()))
            token = self.generate_token(appSecret, file_name, time_stamp)
            jason_data['token'] = token
            jason_data['timestamp'] = time_stamp
            with open(info["file_path"], 'rb') as file:
                file = {'data': (file_name, file.read(), 'multipart/form-data')}
                jason_data_list.append(jason_data)
                file_binaries.append(file)
            #     response = self.m_post(info["url"], session_id=info['session_id'], files=file, data=jason_data)
            #     responses_list.append(response.json())
            # return responses_list
            return jason_data_list, file_binaries

    def split_file(self, file_path, new_dir, chunk_size=10 * 1024 * 1024):
        file_number = 1
        file_parts = []
        with open(file_path, 'rb') as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                file_name = os.path.basename(file_path)
                base, ext = os.path.splitext(file_name)
                chunk_file_name = os.path.join(new_dir, "%s_%d%s" % (base, file_number, ext))
                with open(chunk_file_name, 'wb') as chunk_file:
                    chunk_file.write(chunk)
                file_parts.append(chunk_file_name)
                file_number += 1
        return file_parts

    def generate_token(self, appSecret, filename, timestamp):
        # 拼接字符串
        to_hash = appSecret + "&" + filename + "&" + timestamp
        # 计算token值
        token = self.get_md5sum(to_hash)
        return token

    def get_md5sum(self, file):
        return hashlib.md5(file.encode()).hexdigest()

    def m_post(self, url, session_id=None, files=None, data=None, json=None, **kwargs):
        if session_id is None:
            response = requests.post(url, data=data, json=json, files=files, **kwargs)
            return response
        else:
            headers = {'Sessionid': session_id}
            response = requests.post(url, data=data, json=json, files=files, headers=headers, **kwargs)
            return response

    def m_get(self, url, session_id=None, params=None, **kwargs):
        if session_id is None:
            response = requests.get(url, params=params, **kwargs)
            return response
        else:
            headers = {'Sessionid': session_id}
            response = requests.get(url, params=params, headers=headers, **kwargs)
            return response

    def m_delete(self, url, session_id, json=None, **kwargs):
        headers = {'Sessionid': session_id}
        response = requests.delete(url, json=json, headers=headers, **kwargs)
        return response

    def remove_special_char(self, string):
        return string.replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "")


if __name__ == '__main__':
    public = public_()
    md5, timest = public.generate_token("c9537edd37521e415460b45b25a7ffdc", "wifi_analyze.apk")
    print(md5)
    print(timest)
