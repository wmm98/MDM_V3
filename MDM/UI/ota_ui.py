import os

import requests
from Demos.win32ts_logoff_disconnected import session
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QHBoxLayout, QCheckBox, QComboBox, QButtonGroup, QWidget, QSplitter, QTextEdit, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import pyqtSlot, pyqtSignal
import shutil
import config_path
import configfile
from pubilc import public_
from request_thread import *
from interface_config import HttpInterfaceConfig

conf_path = config_path.UIConfigPath()
pul = public_()


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
        self.verticalLayout_left.addWidget(QLabel())

        # 显示接口中的前10页的ota包，在可选框中显示这些包
        self.verticalLayout_left.addWidget(QLabel("已上传的OTA列表："))
        layout_ota_info = QHBoxLayout()
        self.ota_list_box = QComboBox()
        self.ota_list_box.setFixedWidth(central_length // 2 + 100)
        # self.get_ota_list_button = QtWidgets.QPushButton("获取ota列表")
        self.delete_ota_button = QtWidgets.QPushButton("删除ota")
        # self.delete_all = QtWidgets.QPushButton("删除全部")
        layout_ota_info.addWidget(self.ota_list_box)
        # layout_ota_info.addWidget(self.get_ota_list_button)
        layout_ota_info.addWidget(self.delete_ota_button)
        # layout_ota_info.addWidget(self.delete_all)
        layout_ota_info.addStretch(1)
        self.verticalLayout_left.addLayout(layout_ota_info)
        self.verticalLayout_left.addWidget(QLabel())

        # 选择ota安装方式
        self.verticalLayout_left.addWidget(QLabel("选择OTA安装方式："))
        layout_install_way = QHBoxLayout()
        self.install_way_group = QButtonGroup()
        # self.install_way_group.setExclusive(True)
        self.install_not_silent = QCheckBox("静默安装")
        self.install_part_silent = QCheckBox("半静默安装")
        layout_install_way.addWidget(self.install_not_silent)
        layout_install_way.addWidget(self.install_part_silent)
        layout_install_way.addStretch(1)
        self.verticalLayout_left.addLayout(layout_install_way)
        self.verticalLayout_left.addWidget(QLabel())
        # 只能选择一种方式安装
        self.install_way_group.addButton(self.install_not_silent)
        self.install_way_group.addButton(self.install_part_silent)


        # 设置压测次数
        layout_test_time_info = QHBoxLayout()
        self.test_times_label = QLabel("压测次数")
        self.test_times = QComboBox()
        self.test_times.setEditable(True)
        probability_test_label = QLabel("是否进行失败概率性统计")
        self.is_probability_test = QCheckBox()
        layout_test_time_info.addWidget(self.test_times_label)
        layout_test_time_info.addWidget(self.test_times)
        layout_test_time_info.addWidget(probability_test_label)
        layout_test_time_info.addWidget(self.is_probability_test)
        layout_test_time_info.addStretch(1)
        self.verticalLayout_left.addLayout(layout_test_time_info)
        self.verticalLayout_left.addWidget(QLabel())

        self.submit_button  = QPushButton("保存配置")
        self.verticalLayout_left.addWidget(self.submit_button)
        self.verticalLayout_left.addWidget(QLabel())
        self.verticalLayout_left.addWidget(QLabel())

        self.tips = QLabel("提示：\n请先在主界面登录再进行操作")
        # 设置label字体颜色
        self.tips.setStyleSheet("color:red")
        self.verticalLayout_left.addWidget(self.tips)

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
        if self.ui_config.option_exist(self.ui_config.section_ui_to_background, self.ui_config.option_session_id):
            self.list_ota_packages()
        # self.get_ota_list_button.clicked.connect(self.list_ota_packages)
        self.submit_button.clicked.connect(self.handle_submit)
        # self.stop_process_button.clicked.connect(self.handle_stop)
        # self.login_button.clicked.connect(self.handle_login)
        # self.captcha_button.clicked.connect(self.handle_captcha)
        self.select_button.clicked.connect(self.handle_select)
        self.upload_button.clicked.connect(self.handle_upload)
        self.delete_ota_button.clicked.connect(self.handle_delete_ota)

    def handle_delete_ota(self):
        self.ota_id_flag = 0
        if self.ota_list_box.currentText():
            self.delete_ota_name = os.path.basename(self.ota_list_box.currentText())
            # 先查询ota包，获取ota_id
            self.query_ota_package()

    def delete_ota_package(self, ota_id):
        url = HttpInterfaceConfig.test_delete_ota_address
        th_info = {}
        th_info["url"] = url
        th_info["session_id"] = self.ui_config.get_option_value(self.ui_config.section_ui_to_background,
                                                                self.ui_config.option_session_id)
        json = {}
        json["isSiSafe"] = False
        json["ids"] = [ota_id]
        th_info["json"] = json

        self.delete_worker = DeleteRequestWorker(th_info)
        self.delete_worker.progress.connect(self.handle_delete_ota_response)
        self.delete_worker.start()

    def handle_delete_ota_response(self, json_data):
        if "error" not in json_data:
            if json_data["code"] == 100000:
                self.list_ota_packages()
                QMessageBox.information(None, "提示", "删除ota包成功")
                return
            else:
                QMessageBox.warning(None, "提示", "%s" % json_data["message"])
        else:
            QMessageBox.warning(None, "提示", "删除ota包失败：%s" % json_data["error"])

    def query_ota_package(self):
        url = HttpInterfaceConfig.test_get_ota_list_address
        th_info = {}
        th_info["url"] = url
        th_info["session_id"] = self.ui_config.get_option_value(self.ui_config.section_ui_to_background,
                                                                self.ui_config.option_session_id)
        param = {}
        param["page"] = 1
        param["pageSize"] = 10
        param["order"] = "id"
        param["sort"] = "desc"
        param["departmentId"] = int(self.ui_config.get_option_value(self.ui_config.section_ui_to_background,
                                                               self.ui_config.option_department_id))
        th_info["params"] = param

        self.query_worker = GetRequestWorker(th_info)
        self.query_worker.progress.connect(self.handle_query_response)
        self.query_worker.start()

    def handle_query_response(self, json_data):
        if self.ota_id_flag < 10:
            if "error" not in json_data:
                if json_data["code"] == 100000:
                    if json_data["data"]["otas"] is not None:
                        self.ota_id_flag += 1
                        for pack in json_data["data"]["otas"]:
                            if pack["name"] == os.path.basename(self.ota_list_box.currentText()):
                                ota_id = pack["id"]
                                self.delete_ota_package(ota_id)
                else:
                    QtWidgets.QMessageBox.warning(None, "提示", "%s" % json_data["message"])
            else:
                QtWidgets.QMessageBox.warning(None, "提示", "查询ota包失败：%s" % json_data["error"])
        else:
            QtWidgets.QMessageBox.warning(None, "提示", "查询ota包失败：%s" % json_data["error"])

    def list_test_times(self):
        test_times = [str(i * 5) for i in range(1, 500)]
        self.test_times.addItems(test_times)

    def list_ota_packages(self):
        self.ota_list_flag = 1
        self.ota_packages_list = []
        self.start_next_get_ota_list()

    def start_next_get_ota_list(self):
        thr_info = {}
        url = HttpInterfaceConfig.test_get_ota_list_address
        thr_info["url"] = url
        param = {}
        param["page"] = self.ota_list_flag
        param["pageSize"] = 10
        departmentID = int(self.ui_config.get_option_value(self.ui_config.section_ui_to_background,
                                                           self.ui_config.option_department_id))
        param["departmentId"] = departmentID
        param["order"] = "id"
        param["sort"] = "desc"
        thr_info["params"] = param

        session_id = self.ui_config.get_option_value(self.ui_config.section_ui_to_background, self.ui_config.option_session_id)
        thr_info["session_id"] = session_id
        self.otas_worker = GetRequestWorker(thr_info)
        self.otas_worker.progress.connect(self.handle_ota_list_response)
        self.otas_worker.start()

    def handle_ota_list_response(self, json_data):
        if self.ota_list_flag < 10:
            if "error" not in json_data:
                if json_data["code"] == 100000:
                    if json_data["data"]['otas'] is not None:
                        self.ota_list_flag += 1
                        for pack in json_data["data"]["otas"]:
                            self.ota_packages_list.append(pack["name"])
                    else:
                        self.ota_list_box.clear()
                        self.ota_list_box.addItems(self.ota_packages_list)
                        return

                    self.start_next_get_ota_list()

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
        url = HttpInterfaceConfig.test_upload_ota_address
        # url, file_path, split_file_dir, session_id
        ota_info["url"] = url
        ota_info["file_path"] = file_new_path
        ota_info["file_dir"] = conf_path.ota_split_path
        self.session_id = self.ui_config.get_option_value(self.ui_config.section_ui_to_background,
                                                     self.ui_config.option_session_id)
        ota_info["session_id"] = self.session_id
        self.json_data_list, self.file_binaries = pul.upload_lot(ota_info)
        self.upload_flag = 0
        self.current_upload_index = 0
        self.start_next_upload()

    def start_next_upload(self):
        url = HttpInterfaceConfig.test_upload_ota_address
        if self.current_upload_index < len(self.json_data_list):
            thread_info = {}
            thread_info["data"] = self.json_data_list[self.current_upload_index]
            thread_info["url"] = url
            thread_info["session_id"] = self.ui_config.get_option_value(self.ui_config.section_ui_to_background,
                                                                        self.ui_config.option_session_id)
            thread_info["files"] = self.file_binaries[self.current_upload_index]
            self.worker = PostRequestWorker(thread_info)
            self.worker.progress.connect(self.upload_response)
            self.worker.start()

    def upload_response(self, json_data):
        if "error" not in json_data:
            if json_data["code"] == 100000:
                self.upload_flag += 1
            self.current_upload_index += 1
            self.start_next_upload()

            if self.current_upload_index == len(self.json_data_list):
                self.parsing_ota_package(json_data)
        else:
            QtWidgets.QMessageBox.warning(None, "提示", json_data["error"])
            return

    def parsing_ota_package(self, json_data):
        url = HttpInterfaceConfig.test_parse_ota_address
        th_info = {}
        data = {}
        department_id = int(self.ui_config.get_option_value(self.ui_config.section_ui_to_background, self.ui_config.option_department_id))
        data["departmentId"] = department_id
        data["url"] = json_data["data"]["destination"]
        th_info["json"] = data
        th_info["url"] = url
        th_info["session_id"] = self.ui_config.get_option_value(self.ui_config.section_ui_to_background, self.ui_config.option_session_id)
        self.parase_worker = PostRequestWorker(th_info)
        self.parase_worker.progress.connect(self.handle_parsing_response)
        self.parase_worker.start()

    def handle_parsing_response(self, json_data):
        if "error" not in json_data:
            if json_data["code"] == 100000:
                self.update_ota_package(json_data)
        else:
            QMessageBox.warning(None, "提示", json_data["error"])

    def update_ota_package(self, json_data):
        url = HttpInterfaceConfig.test_update_ota_address
        th_info = {}
        data = {}
        department_id = self.ui_config.get_option_value(self.ui_config.section_ui_to_background,
                                                        self.ui_config.option_department_id)
        data["departmentId"] = int(department_id)
        data["description"] = ""
        data["downloadUrl"] = json_data["data"]["downloadUrl"]
        data["devModel"] = json_data["data"]["devModel"]
        data["downloadUrl"] = json_data["data"]["downloadUrl"]
        data["firmwareVersion"] = json_data["data"]["firmwareVersion"]
        data["md5Sum"] = json_data["data"]["md5Sum"]
        data["name"] = json_data["data"]["name"]
        data["otaType"] = 0
        data["size"] = json_data["data"]["size"]
        data["systemVersion"] = json_data["data"]["systemVersion"]
        data["version"] = json_data["data"]["version"]
        data["wirelessModule"] = json_data["data"]["wirelessModule"]

        th_info["json"] = data
        th_info["url"] = url
        th_info["session_id"] = self.ui_config.get_option_value(self.ui_config.section_ui_to_background,
                                                                self.ui_config.option_session_id)
        self.update_worker = PostRequestWorker(th_info)
        self.update_worker.progress.connect(self.handle_update_response)
        self.update_worker.start()

    def handle_update_response(self, json_data):
        if "error" not in json_data:
            if json_data["code"] == 100000:
                self.list_ota_packages()
                QMessageBox.information(None, "提示", "ota包上传成功")
                return
            else:
                QMessageBox.warning(None, "提示", "%s" % json_data["message"])
        else:
            QMessageBox.warning(None, "提示", "ota上传失败：%s" % json_data["error"])

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
