import os
import requests
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QHBoxLayout, QCheckBox, QComboBox, QButtonGroup, QWidget, QSplitter, QTextEdit, QPushButton, QLabel, QMessageBox, QListView
from PyQt5.QtCore import pyqtSlot, pyqtSignal
import shutil
import config_path
import configfile
from pubilc import public_
from request_thread import *
from interface_config import HttpInterfaceConfig
from configfile import ConfigP


conf_path = config_path.UIConfigPath()
pul = public_()


class APK_MainWindow(config_path.UIConfigPath):
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

        label_apk = QtWidgets.QLabel("apk路径:")
        self.verticalLayout_left.addWidget(label_apk)

        apk_info_layout = QHBoxLayout()
        self.apk_edit = QtWidgets.QLineEdit()
        self.apk_edit.setFixedWidth(central_length // 2 + 100)
        self.select_button = QtWidgets.QPushButton('选择')
        self.upload_button = QtWidgets.QPushButton('上传')
        self.upload_tips = QtWidgets.QLabel("未上传")
        self.upload_tips.setStyleSheet("color:red")
        apk_info_layout.addWidget(self.apk_edit)
        apk_info_layout.addWidget(self.select_button)
        apk_info_layout.addWidget(self.upload_button)
        apk_info_layout.addWidget(self.upload_tips)
        apk_info_layout.addStretch(1)
        self.verticalLayout_left.addLayout(apk_info_layout)
        self.verticalLayout_left.addWidget(QLabel())

        # 显示接口中的前10页的apk包，在可选框中显示这些包
        self.verticalLayout_left.addWidget(QLabel("已上传的apk列表，请选择需要测试的apk包："))
        layout_apk_info = QHBoxLayout()

        # self.apk_list_box = QListView(self)
        # self.apk_list_box.setSelectionMode(QListView.MultiSelection)
        # self.apk_list_box.setFixedWidth(central_length // 2 + 100)

        self.apk_list_box = QtWidgets.QListWidget()
        self.apk_list_box.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)

        self.get_apk_list_button = QtWidgets.QPushButton("获取apk列表")
        self.delete_apk_button = QtWidgets.QPushButton("删除apk")
        self.delete_tips = QtWidgets.QLabel("")
        self.delete_tips.setStyleSheet("color:red")
        # self.delete_all = QtWidgets.QPushButton("删除全部")
        layout_apk_info.addWidget(self.apk_list_box)
        layout_apk_info.addWidget(self.get_apk_list_button)
        layout_apk_info.addWidget(self.delete_apk_button)
        layout_apk_info.addWidget(self.delete_tips)
        # layout_apk_info.addWidget(self.delete_all)
        layout_apk_info.addStretch(1)
        self.verticalLayout_left.addLayout(layout_apk_info)
        self.verticalLayout_left.addWidget(QLabel())

        # # 选择apk安装方式
        # self.verticalLayout_left.addWidget(QLabel("选择apk安装方式："))
        # layout_install_way = QHBoxLayout()
        # self.install_way_group = QButtonGroup()
        # # self.install_way_group.setExclusive(True)
        # self.install_not_silent = QCheckBox("非静默安装")
        # self.install_part_silent = QCheckBox("半静默安装")
        # layout_install_way.addWidget(self.install_not_silent)
        # layout_install_way.addWidget(self.install_part_silent)
        # layout_install_way.addStretch(1)
        # self.verticalLayout_left.addLayout(layout_install_way)
        # self.verticalLayout_left.addWidget(QLabel())
        # # 只能选择一种方式安装
        # self.install_way_group.addButton(self.install_not_silent)
        # self.install_way_group.addButton(self.install_part_silent)

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
        MainWindow.setWindowTitle(_translate("MainWindow", "apk静默升级压测界面"))


class APK_UI(QtWidgets.QMainWindow, APK_MainWindow):
    def __init__(self):
        super(APK_UI, self).__init__()
        self.ui_config = configfile.ConfigP(self.ui_config_file_path)
        self.setupUi(self)
        self.clear_package_path()
        self.init_ui()
        self.init_signal_slot()
        self.submit_flag = False

    def init_ui(self):
        if self.ui_config.option_exist(self.ui_config.section_ui_to_background, self.ui_config.option_session_id):
            self.list_apk_packages()
        self.list_test_times()

    def init_signal_slot(self):
        self.get_apk_list_button.clicked.connect(self.list_apk_packages)
        self.submit_button.clicked.connect(self.handle_submit)
        # self.stop_process_button.clicked.connect(self.handle_stop)
        # self.login_button.clicked.connect(self.handle_login)
        # self.captcha_button.clicked.connect(self.handle_captcha)
        self.select_button.clicked.connect(self.handle_select)
        self.upload_button.clicked.connect(self.handle_upload)
        self.delete_apk_button.clicked.connect(self.handle_delete_apk)

    def clear_package_path(self):
        original_path = conf_path.apk_origin_path
        split_path = conf_path.apk_split_path
        # 删除文件夹下面的所有文件
        for file in os.listdir(original_path):
            os.remove(os.path.join(original_path, file))
        for file in os.listdir(split_path):
            os.remove(os.path.join(split_path, file))

    def handle_delete_apk(self):
        if not self.apk_list_box.selectedItems():
            QtWidgets.QMessageBox.warning(None, "提示", "请选择需要删除的apk包")
            return

        self.apk_id_flag = 0
        apk_delete_ids = []
        selected_items = self.apk_list_box.selectedItems()
        self.selected_texts = [item.text() for item in selected_items]
        print(self.selected_texts)
        for text in self.selected_texts:
            # 先查询apk包，获取apk_id
            if text in self.apks_info_dict:
                apk_id = self.apks_info_dict[text][0]
                apk_delete_ids.append(apk_id)
                print(apk_delete_ids)
                self.delete_apk_package(apk_id)
            # self.query_apk_package()
        self.delete_tips.setText("已成功删除选中的apk包")
        self.list_apk_packages()

    def delete_apk_package(self, apk_id):
        url = HttpInterfaceConfig.test_delete_apk_address
        th_info = {}
        th_info["url"] = url
        th_info["session_id"] = self.ui_config.get_option_value(self.ui_config.section_ui_to_background,
                                                                self.ui_config.option_session_id)
        json = {}
        json["isSiSafe"] = False
        json["ids"] = [apk_id]
        th_info["json"] = json

        self.delete_worker = DeleteRequestWorker(th_info)
        self.delete_worker.progress.connect(self.handle_delete_apk_response)
        self.delete_worker.start()

    def handle_delete_apk_response(self, json_data):
        if "error" not in json_data:
            if json_data["code"] == 100000:
                pass
            else:
                QMessageBox.warning(None, "提示", "%s" % json_data["message"])
                return
        else:
            QMessageBox.warning(None, "提示", "删除apk包失败：%s" % json_data["error"])
            return

    def query_apk_package(self):
        url = HttpInterfaceConfig.test_get_apk_list_address
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
        if self.apk_id_flag != -1:
            if "error" not in json_data:
                if json_data["code"] == 100000:
                    if json_data["data"]["apks"] is not None:
                        self.apk_id_flag += 1
                        for pack in json_data["data"]["apks"]:
                            if pack["appName"] in self.selected_texts:
                                apk_id = pack["id"]
                                self.delete_apk_package(apk_id)
                    else:
                        self.apk_id_flag = -1
                else:
                    QtWidgets.QMessageBox.warning(None, "提示", "%s" % json_data["message"])
                    return
            else:
                QtWidgets.QMessageBox.warning(None, "提示", "查询apk包失败：%s" % json_data["error"])
                return
        else:
            QtWidgets.QMessageBox.warning(None, "提示", "查询apk包失败：%s" % json_data["error"])
            return

    def list_apk_packages(self):
        self.apk_list_box.clear()
        self.apk_list_flag = 1
        # self.apk_packages_list = []
        # self.apk_package_ids_list = []
        # self.apk_packages_name_list = []
        self.apks_info_dict = {}
        self.start_next_get_apk_list()

    def start_next_get_apk_list(self):
        thr_info = {}
        url = HttpInterfaceConfig.test_get_apk_list_address
        thr_info["url"] = url
        param = {}
        param["page"] = self.apk_list_flag
        param["pageSize"] = 10
        departmentID = int(self.ui_config.get_option_value(self.ui_config.section_ui_to_background,
                                                           self.ui_config.option_department_id))
        param["departmentId"] = departmentID
        param["order"] = "id"
        param["sort"] = "desc"
        thr_info["params"] = param

        session_id = self.ui_config.get_option_value(self.ui_config.section_ui_to_background, self.ui_config.option_session_id)
        thr_info["session_id"] = session_id
        self.apks_worker = GetRequestWorker(thr_info)
        self.apks_worker.progress.connect(self.handle_apk_list_response)
        self.apks_worker.start()

    def handle_apk_list_response(self, json_data):
        print("===========apk列表===========")
        print(json_data)
        if self.apk_list_flag != -1:
            if "error" not in json_data:
                if json_data["code"] == 100000:
                    if json_data["data"]['apks'] is not None:
                        self.apk_list_flag += 1
                        for pack in json_data["data"]["apks"]:
                            self.apks_info_dict[pack["appName"]] = [pack["id"], pack["pkgName"]]
                            print(self.apks_info_dict)
                    else:
                        self.apk_list_flag = -1
                        if self.apks_info_dict:
                            # 添加到apk列表框中
                            self.apk_list_box.clear()
                            self.apk_list_box.addItems(list(self.apks_info_dict.keys()))

                    self.start_next_get_apk_list()

    def handle_submit(self):
        if not self.apk_list_box.selectedItems() or len(self.apk_list_box.selectedItems()) > 1:
            QtWidgets.QMessageBox.warning(None, "提示", "请选择一个app进行测试")
            return
        #
        # if not self.install_way_group.checkedButton():
        #     QtWidgets.QMessageBox.warning(None, "提示", "请选择apk升级方式")
        #     return
        if not self.test_times.currentText():
            QtWidgets.QMessageBox.warning(None, "提示", "请选择测试次数")
            return
        # 保存配置
        self.save_config()
        self.submit_flag = True
        QtWidgets.QMessageBox.information(None, "提示", "apk包压测例配置保存成功")

    def save_config(self):
        config = ConfigP(self.ui_config_file_path)
        section = config.section_apk_silent_upgrade
        config.add_config_section(section)

        selected_items = self.apk_list_box.selectedItems()
        self.selected_texts = [item.text() for item in selected_items]
        test_app_name = self.selected_texts[0]

        for app_ in self.apks_info_dict:
            if app_ == test_app_name:
                apk_id = self.apks_info_dict[app_][0]
                apk_pkg_name = self.apks_info_dict[app_][1]
                self.ui_config.add_config_option(section, self.ui_config.option_apk_package_name, apk_pkg_name)
                self.ui_config.add_config_option(section, self.ui_config.option_apk_id, str(apk_id))

        # if self.install_not_silent.isChecked():
        #     config.add_config_option(section, config.option_apk_is_not_silent, "1")
        # else:
        #     config.add_config_option(section, config.option_apk_is_not_silent, "0")
        # if self.install_part_silent.isChecked():
        #     config.add_config_option(section, config.option_apk_is_part_silent, "1")
        # else:
        #     config.add_config_option(section, config.option_apk_is_part_silent, "0")

        config.add_config_option(section, config.test_times, self.test_times.currentText())

        if self.is_probability_test.isChecked():
            config.add_config_option(section, config.is_probability_test, "1")
        else:
            config.add_config_option(section, config.is_probability_test, "0")

    def handle_stop(self):
        pass

    def handle_upload(self):
        if not self.apk_edit.text():
            QtWidgets.QMessageBox.warning(None, "提示", "请选择APK文件")
            return
        self.upload_tips.setText("开始上传...")
        file_name = self.apk_edit.text()
        file_new_path = os.path.join(conf_path.apk_origin_path, os.path.basename(file_name))
        shutil.copy(file_name, file_new_path)
        # 最多按照10M进行分块上传
        apk_info = {}
        url = HttpInterfaceConfig.test_upload_apk_address
        # url, file_path, split_file_dir, session_id
        apk_info["url"] = url
        apk_info["file_path"] = file_new_path
        apk_info["file_dir"] = conf_path.apk_split_path
        self.session_id = self.ui_config.get_option_value(self.ui_config.section_ui_to_background,
                                                     self.ui_config.option_session_id)
        apk_info["session_id"] = self.session_id
        self.json_data_list, self.file_binaries = pul.upload_lot(apk_info)
        self.upload_flag = 0
        self.current_upload_index = 0
        self.start_next_upload()

    def start_next_upload(self):
        url = HttpInterfaceConfig.test_upload_apk_address
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
        print(json_data)
        if "error" not in json_data:
            if json_data["code"] == 100000:
                self.upload_flag += 1
                self.upload_tips.setText("第%d片上传成功！" % self.current_upload_index)
                self.current_upload_index += 1
                self.start_next_upload()
            else:
                QtWidgets.QMessageBox.warning(None, "提示", "%s" % json_data["message"])
                return
            if self.current_upload_index == len(self.json_data_list):
                self.parsing_apk_package(json_data)
        else:
            QtWidgets.QMessageBox.warning(None, "提示", json_data["error"])
            return

    def parsing_apk_package(self, json_data):
        url = HttpInterfaceConfig.test_parse_apk_address
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
        print(json_data)
        if "error" not in json_data:
            if json_data["code"] == 100000:
                # QtWidgets.QMessageBox.information(None, "提示", "apk包解析成功")
                self.upload_tips.setText("apk解析成功")
                self.update_apk_package(json_data)
            else:
                QtWidgets.QMessageBox.warning(None, "提示", "%s" % json_data["message"])
                return
        else:
            QMessageBox.warning(None, "提示", json_data["error"])
            return

    def update_apk_package(self, json_data):
        print("================更新记录================")
        print(json_data)
        url = HttpInterfaceConfig.test_update_apk_address
        th_info = {}
        data = {}
        department_id = self.ui_config.get_option_value(self.ui_config.section_ui_to_background,
                                                        self.ui_config.option_department_id)
        data["apkPath"] = json_data["data"]["downloadUrl"]
        data["appCate"] = 7
        data["appName"] = json_data["data"]["appName"]
        data["appPushShop"] = 0
        data["appType"] = 0
        data["departmentId"] = int(department_id)
        data["description"] = ""
        data["downloadUrl"] = json_data["data"]["downloadUrl"]
        data["image"] = json_data["data"]["image"]
        data["md5Sum"] = json_data["data"]["md5Sum"]
        data["pkgName"] = json_data["data"]["pkgName"]
        data["size"] = json_data["data"]["size"]
        data["version"] = json_data["data"]["version"]
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
                self.upload_tips.setText("apk更新成功，apk包上传成功")
                self.list_apk_packages()
                # QMessageBox.information(None, "提示", "apk更新成功，apk包上传成功")
            else:
                QMessageBox.warning(None, "提示", "%s" % json_data["message"])
                return
        else:
            QMessageBox.warning(None, "提示", "apk上传失败：%s" % json_data["error"])
            return

    def handle_select(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(None, "选择apk文件", "", "APK Files (*.apk)",
                                                             options=self.options)
        self.apk_edit.setText(file_name)

    def list_test_times(self):
        test_times = [str(i * 3) for i in range(1, 500)]
        self.test_times.addItems(test_times)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    apk_ui = APK_UI()
    apk_ui.show()
    app.exec_()
