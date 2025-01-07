from PyQt5 import QtCore
import config_path
from pubilc import public_
import requests

conf_path = config_path.UIConfigPath()
pul = public_()


class PostRequestWorker(QtCore.QThread):
    progress = QtCore.pyqtSignal(dict)  # 修改信号类型为字典

    def __init__(self, info):
        super().__init__()
        self.info = info

    def run(self):
        try:
            if "files" in self.info:
                response = pul.m_post(url=self.info["url"], data=self.info["data"], session_id=self.info["session_id"],
                                      files=self.info["files"])
            else:
                response = pul.m_post(url=self.info["url"], json=self.info["json"], session_id=self.info["session_id"])
            response.raise_for_status()  # 检查 HTTP 请求是否成功
            json_data = response.json()  # 解析返回的 JSON 数据
            self.progress.emit(json_data)  # 发射 JSON 数据
        except requests.RequestException as e:
            self.progress.emit({"error": str(e)})  # 处理请求错误并发射错误信息


class GetRequestWorker(QtCore.QThread):
    progress = QtCore.pyqtSignal(dict)

    def __init__(self, info):
        super().__init__()
        self.info = info

    def run(self):
        try:
            response = pul.m_get(url=self.info["url"], session_id=self.info["session_id"], params=self.info["params"])
            response.raise_for_status()  # 检查 HTTP 请求是否成功
            json_data = response.json()  # 解析返回的 JSON 数据
            self.progress.emit(json_data)  # 发射 JSON 数据
        except requests.RequestException as e:
            self.progress.emit({"error": str(e)})  # 处理请求错误并发射错误信息


class DeleteRequestWorker(QtCore.QThread):
    progress = QtCore.pyqtSignal(dict)

    def __init__(self, info):
        super().__init__()
        self.info = info

    def run(self):
        try:
            response = pul.m_delete(url=self.info["url"], session_id=self.info["session_id"], json=self.info["json"])
            response.raise_for_status()  # 检查 HTTP 请求是否成功
            json_data = response.json()  # 解析返回的 JSON 数据
            self.progress.emit(json_data)  # 发射 JSON 数据
        except requests.RequestException as e:
            self.progress.emit({"error": str(e)})  # 处理请求错误并发射错误信息
