import os

import requests
from Demos.win32ts_logoff_disconnected import session
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QHBoxLayout, QCheckBox, QComboBox, QButtonGroup, QWidget, QSplitter, QTextEdit
from PyQt5.QtCore import pyqtSlot, pyqtSignal
import shutil
import config_path
import configfile
from pubilc import public_

conf_path = config_path.UIConfigPath()
pul = public_()


class PostRequestWorker(QtCore.QThread):
    progress = QtCore.pyqtSignal(dict)  # 修改信号类型为字典

    def __init__(self, info):
        super().__init__()
        self.info = info

    def run(self):
        try:
            response = pul.m_post(url=self.info["url"], data=self.info["data"], session_id=self.info["session_id"], files=self.info["files"])
            response.raise_for_status()  # 检查 HTTP 请求是否成功
            json_data = response.json()  # 解析返回的 JSON 数据
            self.progress.emit(json_data)  # 发射 JSON 数据
        except requests.RequestException as e:
            self.progress.emit({"error": str(e)})  # 处理请求错误并发射错误信息



class OTA_MainWindow(config_path.UIConfigPath):
    options = QtWidgets.QFileDialog.Options()
    options |= QtWidgets.QFileDialog.ReadOnly

    def __init__(self):
        pass

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        central_length = 700
        central_width = 500
        MainWindow.resize(central_length, central_width)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.main_layout = QHBoxLayout(self.centralwidget)
        splitter = QSplitter()
        self.main_layout.addWidget(splitter)

        left_widget = QWidget()
        self.verticalLayout_left = QtWidgets.QVBoxLayout(left_widget)

        label_ota = QtWidgets.QLabel("OTA路径:")
        self.verticalLayout_left.addWidget(label_ota)

        ota_info_layout = QHBoxLayout()
        self.ota_edit = QtWidgets.QLineEdit()
        self.ota_edit.setFixedWidth(central_length // 2 + 100)
        self.select_button = QtWidgets.QPushButton('选择')
        self.upload_button = QtWidgets.QPushButton('上传')
        ota_info_layout.addWidget(self.ota_edit)
        ota_info_layout.addWidget(self.select_button)
        ota_info_layout.addWidget(self.upload_button)
        ota_info_layout.addStretch(1)
        self.verticalLayout_left.addLayout(ota_info_layout)

        self.verticalLayout_left.addStretch(1)
        self.verticalLayout_left.setSpacing(10)  # 崔直布局的间距为10像素

        splitter.addWidget(left_widget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "OTA升级压测界面"))


class OTA_UI(QtWidgets.QMainWindow, OTA_MainWindow):
    def __init__(self):
        super(OTA_UI, self).__init__()
        self.ui_config = configfile.ConfigP(self.ui_config_file_path)
        self.setupUi(self)
        self.init_ui()
        self.init_signal_slot()

    def init_ui(self):
        pass

    def init_signal_slot(self):
        # self.submit_button.clicked.connect(self.handle_submit)
        # self.stop_process_button.clicked.connect(self.handle_stop)
        # self.login_button.clicked.connect(self.handle_login)
        # self.captcha_button.clicked.connect(self.handle_captcha)
        self.select_button.clicked.connect(self.handle_select)
        self.upload_button.clicked.connect(self.handle_upload)

    def handle_submit(self):
        pass

    def handle_stop(self):
        pass

    def handle_upload(self):
        if not self.ota_edit.text():
            QtWidgets.QMessageBox.warning(None, "提示", "请选择OTA文件")
            return
        file_name = self.ota_edit.text()
        file_new_path = os.path.join(conf_path.ota_origin_path, os.path.basename(file_name))
        shutil.copy(file_name, file_new_path)
        # 最多按照10M进行分块上传
        ota_info = {}
        url = "http://192.168.0.30:8080/api/v1/upload/ota"
        # url, file_path, split_file_dir, session_id
        ota_info["url"] = url
        ota_info["file_path"] = file_new_path
        ota_info["file_dir"] = conf_path.ota_split_path
        session_id = self.ui_config.get_option_value(self.ui_config.section_ui_to_background,
                                                     self.ui_config.option_session_id)
        ota_info["session_id"] = session_id
        json_data_list, file_binaries = pul.upload_lot(ota_info)
        thread_info = {}
        thread_info["data"] = json_data_list[0]
        thread_info["url"] = url
        thread_info["session_id"] = self.ui_config.get_option_value(self.ui_config.section_ui_to_background,
                                                                   self.ui_config.option_session_id)
        thread_info["files"] = file_binaries[0]

        self.worker = PostRequestWorker(thread_info)
        self.worker.progress.connect(self.upload_response)  # Connect signal to slot
        self.worker.start()

        # [{'code': 100000, 'message': 'success', 'data': {'destination': 'http://192.168.0.32:8000/fileStatic/tmp/55/ota/1_T10_qcm2290_sv12_fv2.1.7_pv2.1.7-9.9.9.zip'}}]

    def upload_response(self, json_data):
        print("=====================")
        print(json_data)

    def handle_select(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(None, "选择OTA文件", "", "Zip Files (*.zip)",
                                                             options=self.options)
        self.ota_edit.setText(file_name)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ota_ui = OTA_UI()
    ota_ui.show()
    app.exec_()
