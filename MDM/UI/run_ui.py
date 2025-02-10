import subprocess
import sys
import base64
import time

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtCore import QProcess, Qt, pyqtSlot
from PyQt5.QtGui import QTextDocument, QTextCursor, QTextImageFormat
from init_ui import Ui_MainWindow
from PyQt5.QtCore import QByteArray, QTimer
from PyQt5.QtGui import QPixmap
import os
import requests
import configfile
import config_path
from interface_config import HttpInterfaceConfig
from ota_ui import OTA_UI
from pubilc import public_
from request_thread import *

conf_path = config_path.UIConfigPath()
pul = public_()


class ComboBoxDelegate(QStyledItemDelegate):
    def __init__(self, items, parent=None):
        super().__init__(parent)
        self.items = items

    def createEditor(self, parent, option, index):
        editor = QComboBox(parent)
        editor.addItems(self.items)
        return editor

    def setEditorData(self, editor, index):
        current_text = index.data()
        editor.setCurrentText(current_text)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentText())


class UIDisplay(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(UIDisplay, self).__init__()
        self.last_position = 0

        self.bg_config = configfile.ConfigP(self.background_config_file_path)
        self.ui_config = configfile.ConfigP(self.ui_config_file_path)

        self.ota_ui = OTA_UI()
        self.setupUi(self)
        self.uuid = None
        self.display_captcha()
        self.AllTestCase = None
        self.device_sn = None
        self.inti_ui()
        self.init_signal_slot()
        self.cases_selected_sum = 0

    def inti_ui(self):
        # 初始化ini文件
        self.ui_config.init_config_file()
        self.ui_config.add_config_section(self.ui_config.section_ui_to_background)
        # 初始化
        # 初始化图片cursor
        # self.cursor = QTextCursor(self.document)
        # self.cursor_camera = QTextCursor(self.document_camera)

        # 初始化进程
        self.qt_process = QProcess()

        # 展示用例树
        self.list_tree_cases()
        self.select_devices_name()
        self.check_device_online()

    def init_signal_slot(self):
        self.treeWidget.expandAll()
        self.treeWidget.itemChanged.connect(self.handlechanged)
        # 用例树点击事件
        self.treeWidget.itemClicked.connect(self.on_item_clicked)
        self.qt_process.finished.connect(self.handle_finished)
        self.captcha_button.clicked.connect(self.display_captcha)
        self.login_button.clicked.connect(self.login)
        self.bind_device_button.clicked.connect(self.bind_device)
        self.switch_server_button.clicked.connect(self.switch_sever)

        self.test_version.clicked.connect(self.display_captcha)
        self.release_version.clicked.connect(self.display_captcha)
        self.display_device_info_button.clicked.connect(self.get_device_status)

        self.edit_device_name.currentIndexChanged.connect(self.get_device_sn)
        self.reboot_device_button.clicked.connect(self.handle_reboot)
        self.submit_button.clicked.connect(self.handle_submit)
        self.stop_process_button.clicked.connect(self.stop_process)

        self.ota_ui.submit_button.clicked.connect(self.display_ota_stability_test_times)

    def display_ota_stability_test_times(self):
        time.sleep(1)
        if self.ota_ui.submit_flag:
            if self.item_S_T_STA_child_ota_test.checkState(0) == 2:
                times = self.ui_config.get_option_value(self.ui_config.section_ota_interface,
                                                        self.ui_config.test_times)
                self.item_S_T_STA_child_ota_test.setText(1, times)
                self.item_S_T_STA_child_ota_test.setTextAlignment(1, Qt.AlignRight)

    def check_device_online(self):
        self.online_timer = QTimer(self)
        self.online_timer.timeout.connect(self.update_devices_box)
        self.online_timer.start(5000)

    def update_devices_box(self):
        devices_list = pul.get_devices_list()
        self.edit_device_name.clear()
        self.edit_device_name.addItems(devices_list)

    def handle_reboot(self):
        device_name = self.edit_device_name.currentText()
        if device_name:
            pul.reboot_device(device_name)
            # pul.restart_adb()

    def switch_sever(self):
        if self.test_version.isChecked():
            url = HttpInterfaceConfig.test_switch_server_address
        else:
            url = HttpInterfaceConfig.release_switch_server_address
        th_info = {}
        th_info["url"] = url
        th_info["session_id"] = self.ui_config.get_option_value(self.ui_config.section_ui_to_background,
                                                                self.ui_config.option_session_id)
        json = {}
        json["sns"] = [self.device_sn]
        json["resetFactoryType"] = "1"
        json["desc"] = ""
        json["departmentId"] = int(self.ui_config.get_option_value(self.ui_config.section_ui_to_background,
                                                                   self.ui_config.option_department_id))
        if self.test_version.isChecked():
            json["url"] = HttpInterfaceConfig.release_server_address
        else:
            json["url"] = HttpInterfaceConfig.test_server_address
        th_info["json"] = json
        self.switch_server_worker = PostRequestWorker(th_info)
        self.switch_server_worker.progress.connect(self.handle_switch_server)
        self.switch_server_worker.start()

    def handle_switch_server(self, json_data):
        if "error" not in json_data:
            if json_data["code"] == 100000:
                QtWidgets.QMessageBox.information(None, "提示", "切换服务器成功")
                return
            else:
                QtWidgets.QMessageBox.warning(None, "提示", "%s" % json_data["message"])
                return
        else:
            QtWidgets.QMessageBox.warning(None, "提示", "切换服务器失败：%s" % json_data["error"])
            return

    def get_device_sn(self):
        # 获取设备sn
        device_name = self.edit_device_name.currentText()
        self.device_sn = pul.remove_special_char(pul.get_device_serial(device_name))

    def get_device_status(self):
        self.device_status_label.setText("正在获取设备状态...")
        self.device_list_flag = 1
        self.start_next_get_devices_list()

    def start_next_get_devices_list(self):
        thr_info = {}
        if self.test_version.isChecked():
            url = HttpInterfaceConfig.test_get_devices_address
        else:
            url = HttpInterfaceConfig.release_get_devices_address
        thr_info["url"] = url
        param = {}
        param["page"] = self.device_list_flag
        param["pageSize"] = 10
        departmentID = int(self.ui_config.get_option_value(self.ui_config.section_ui_to_background,
                                                           self.ui_config.option_department_id))
        param["departmentId"] = departmentID
        param["order"] = "id"
        param["sort"] = "desc"
        thr_info["params"] = param

        session_id = self.ui_config.get_option_value(self.ui_config.section_ui_to_background,
                                                     self.ui_config.option_session_id)
        thr_info["session_id"] = session_id
        self.devices_worker = GetRequestWorker(thr_info)
        self.devices_worker.progress.connect(self.handle_devices_list_response)
        self.devices_worker.start()

    def handle_devices_list_response(self, json_data):
        if self.device_list_flag < 10:
            if "error" not in json_data:
                if json_data["code"] == 100000:
                    if json_data["data"]['total'] > 0:
                        for device_info in json_data["data"]["rows"]:
                            print(device_info["sn"])
                            if device_info["sn"] in self.device_sn:
                                print("查询到设备信息.")
                                self.device_status_label.setText("%s：%s" % (device_info["sn"], device_info["iotStatus"]))
                                return
                        self.device_list_flag += 1
                        self.start_next_get_devices_list()
                    else:
                        self.device_status_label.setText("查询不到设备信息.")
                        return
                else:
                    QtWidgets.QMessageBox.warning(None, "提示", "%s" % json_data["message"])
                    return
            else:
                QtWidgets.QMessageBox.warning(None, "提示", "查询设备信息失败：%s" % json_data["error"])

    def bind_device(self):
        if self.test_version.isChecked():
            url = HttpInterfaceConfig.test_bind_devices_address
        else:
            url = HttpInterfaceConfig.release_bind_devices_address

        th_info = {}
        th_info["url"] = url
        th_info["session_id"] = self.ui_config.get_option_value(self.ui_config.section_ui_to_background,
                                                                self.ui_config.option_session_id)
        json = {}
        json["sn"] = self.device_sn
        json["deviceType"] = 1
        json["departmentId"] = int(self.ui_config.get_option_value(self.ui_config.section_ui_to_background,
                                                                    self.ui_config.option_department_id))
        th_info["json"] = json
        self.bind_worker = PostRequestWorker(th_info)
        self.bind_worker.progress.connect(self.handle_bind_device)
        self.bind_worker.start()

    def handle_bind_device(self, json_data):
        if "error" not in json_data:
            if json_data["code"] == 100000:
                QtWidgets.QMessageBox.information(None, "提示", "绑定设备成功")
                return
            else:
                QtWidgets.QMessageBox.warning(None, "提示", "%s" % json_data["message"])
                return
        else:
            QtWidgets.QMessageBox.warning(None, "提示", "绑定失败：%s" % json_data["error"])
            return

    def login(self):
        # 登录
        username = self.edit_user_name.text()
        if not username:
            self.get_waring("用户名不能为空!!!")
            return
        password = self.edit_password.text()
        if not password:
            self.get_waring("密码不能为空!!!")
            return
        captcha = self.edit_captcha.text()
        if not captcha:
            self.get_waring("验证码不能为空!!!")
            return
        # 登录
        if self.test_version.isChecked():
            url = HttpInterfaceConfig.test_login_address
        else:
            url = HttpInterfaceConfig.release_login_address
        json_data = {"username": username, "password": password, "uuid": self.uuid, "captcha": captcha}
        try:
            response = requests.post(url=url, json=json_data).json()
            if response["code"] == 100000:
                session_id = response["data"]["session_id"]
                department_id = str(response["data"]["user"]["departmentId"])
                self.ui_config.add_config_option(self.ui_config.section_ui_to_background, self.ui_config.option_session_id, session_id)
                self.ui_config.add_config_option(self.ui_config.section_ui_to_background, self.ui_config.option_department_id, department_id)
                self.login_tips.setVisible(True)
                self.login_tips.setText("登录成功！")
                self.login_tips.setStyleSheet("color:red")
                self.get_information("登录成功!")
                # 记录下sn信息
                self.get_device_sn()
                return
            elif response["code"] == 21002:
                self.login_tips.setVisible(True)
                self.login_tips.setText("登录失败，用户名或密码错误，请重新登录!")
                self.login_tips.setStyleSheet("color:red")
                self.get_waring("登录失败，用户名或密码错误，请重新登录!")
                return
            elif response["code"] == 21001:
                self.login_tips.setVisible(True)
                self.login_tips.setText("登录失败，验证码错误，请重新登录!")
                self.login_tips.setStyleSheet("color:red")
                self.get_waring("登录失败，验证码错误，请重新登录!")
                return
            else:
                self.login_tips.setVisible(True)
                self.login_tips.setText("登录失败， 失败码：%s，请重新登录!" % response["code"])
                self.login_tips.setStyleSheet("color:red")
                self.get_waring("登录失败，请重新登录!")
                return
        except Exception as e:
            self.login_tips.setVisible(True)
            self.login_tips.setText("登录失败，，请重新登录!")
            self.login_tips.setStyleSheet("color:red")
            self.get_waring(str(e))
            return

    def get_captcha(self):
        # 获取验证码
        if self.test_version.isChecked():
            url = HttpInterfaceConfig.test_get_captcha_address
        else:
            url = HttpInterfaceConfig.release_get_captcha_address
        print(url)
        response = requests.get(url).json()
        uuid = response["data"]["uuid"]
        captcha_base64 = response["data"]["captcha"]
        self.uuid = uuid
        return {"uuid": uuid, "captcha": captcha_base64}

    def display_captcha(self):
        captcha_info = self.get_captcha()
        self.uuid = captcha_info["uuid"]
        self.captcha = captcha_info["captcha"]
        # 转换为图片格式
        image_data = base64.b64decode(self.captcha)
        byte_array = QByteArray(image_data)
        pixmap = QPixmap()
        pixmap.loadFromData(byte_array)
        self.captcha_button.setPixmap(pixmap)

    def get_information(self, info):
        QMessageBox.information(self, "提示", info)

    def get_waring(self, message):
        QMessageBox.warning(self, "警告", message)

    def select_devices_name(self):
        devices = self.bg_config.get_option_value(self.bg_config.section_background_to_ui,
                                                  self.bg_config.bg_option_devices_name).split(",")
        for device in devices:
            self.edit_device_name.addItem(str(device))

    def handle_finished(self):
        self.stop_process()

    def handle_submit(self):
        # 检查用例是否为空
        self.tree_status = []
        # 用例跑的时间集
        self.tree_values = []
        for i in range(self.treeWidget.topLevelItemCount()):
            item = self.treeWidget.topLevelItem(i)
            # 2 表示已勾选，0 表示未勾选，1 表示半选中
            self.tree_status.append(self.get_tree_item_status(item))

        # 保存要跑的用例
        self.durations = []
        self.cases = []
        tree_status = self.tree_status[0]["children"][0]["children"]

        # 提取压测用例
        for slave in tree_status:
            for children in slave['children']:
                if children["status"] == 2:
                    self.cases.append(children["text"])

        if not self.cases:
            self.get_waring("请选择用例")
            return

        # 相应用例转为英文标识
        self.transfer_cases = []
        for case in self.cases:
            if "OTA推送压测" in case:
                self.transfer_cases.append("stability_normal_release_ota")

        self.ui_config.add_config_option(self.ui_config.section_ui_to_background,
                                         self.ui_config.ui_option_device_name,
                                         self.edit_device_name.currentText())
        # 保存用例
        self.ui_config.add_config_option(self.ui_config.section_ui_to_background,
                                         self.ui_config.ui_option_cases, ",".join(self.transfer_cases))

        self.start_qprocess(conf_path.main_bat_path)

        # 设置定时器检测间隔
        self.check_interval = 1000  # 定时器间隔，单位毫秒
        # 调试日志定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_debug_log)
        self.timer.start(self.check_interval)  # 启动定时器
        # 展示图片的两个定定时器

        self.stop_process_button.setEnabled(True)
        self.submit_button.setDisabled(True)
        self.submit_button.setText("测试中...")

    # 或者使用 QProcess
    def start_qprocess(self, file_path):
        # 启动新进程
        self.qt_process.start(file_path)

    def stop_process(self):
        # 文件位置初始化
        self.force_task_kill()
        self.last_position = 0
        self.stop_process_button.setDisabled(True)
        self.submit_button.setEnabled(True)
        self.submit_button.setText("开始测试")
        self.text_edit.insertPlainText("测试结束\n")
        self.timer.stop()

    def force_task_kill(self):
        self.qt_process.startDetached("taskkill /PID %s /F /T" % str(self.qt_process.processId()))

    def closeEvent(self, event):
        # 在窗口关闭时停止定时器,关闭任务运行
        # 停止 QProcess 进程
        self.qt_process.startDetached("taskkill /PID %s /F /T" % str(self.qt_process.processId()))
        self.timer.stop()
        event.accept()

    def update_debug_log(self):
        try:
            log_file = self.debug_log_path
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as file:
                    file.seek(self.last_position)
                    new_content = file.read()
                    if new_content:
                        self.text_edit.insertPlainText(new_content + "\n")
                        self.last_position = file.tell()
        except Exception as e:
            self.log_edit.insertPlainText(str(e) + "\n")

    def handlechanged(self, item, column):
        # 获取选中节点的子节点个数
        count = item.childCount()
        # 如果选中,子节点全选中
        if item.checkState(column) == Qt.Checked:
            for f in range(count):
                if item.child(f).checkState(0) != Qt.Checked:
                    item.child(f).setCheckState(0, Qt.Checked)
        # 如果取消选中,子节点全取消勾选
        if item.checkState(column) == Qt.Unchecked:
            for f in range(count):
                if item.child(f).checkState != Qt.Unchecked:
                    item.child(f).setCheckState(0, Qt.Unchecked)

    def get_tree_item_status(self, tree_item):
        status = tree_item.checkState(0)
        if status == 2:
            self.cases_selected_sum += 1
        result = {
            "text": tree_item.text(0),
            "status": status,
            "children": [],
            "duration": tree_item.text(1)
        }
        for i in range(tree_item.childCount()):
            child_item = tree_item.child(i)
            result["children"].append(self.get_tree_item_status(child_item))
        return result

    def on_item_clicked(self, item):
        # 查看ini文件中登录的个人信息是否存在

        if not self.ui_config.option_exist(self.ui_config.section_ui_to_background, self.ui_config.option_session_id):
            # 如果没有登录，清除已选的用例
            item.setCheckState(0, Qt.Unchecked)
            QMessageBox.warning(self, "警告", "请先登录")
            return

        if item == self.item_S_T_STA_child_ota_test:
            if item.checkState(0) == 2:
                if not self.ota_ui.isVisible():
                    self.ota_ui.show()

    def list_tree_cases(self):
        # 用例数结构
        # 设置列数
        self.treeWidget.setColumnCount(3)
        # 设置树形控件头部的标题
        self.treeWidget.setHeaderLabels(['测试场景', "运行时长/轮数", "单位"])
        self.treeWidget.setColumnWidth(0, 450)

        # 设置根节点
        self.AllTestCase = QTreeWidgetItem(self.treeWidget)
        # self.case_tree = self.AllTestCase.child()
        self.AllTestCase.setText(0, '测试项')

        # 压测根节点
        self.item_sta_root = QTreeWidgetItem(self.AllTestCase)
        self.item_sta_root.setText(0, "压测")
        self.item_sta_root.setFlags(self.item_sta_root.flags() | Qt.ItemIsSelectable)
        # 立项测试
        self.item_S_T_STA = QTreeWidgetItem(self.item_sta_root)
        self.item_S_T_STA.setText(0, "压测")
        self.item_S_T_STA.setCheckState(0, Qt.Unchecked)
        self.item_S_T_STA.setFlags(self.item_S_T_STA.flags() | Qt.ItemIsSelectable)
        # 立项测试子用例
        self.item_S_T_STA_child_ota_test = QTreeWidgetItem(self.item_S_T_STA)
        self.item_S_T_STA_child_ota_test.setText(0, "OTA推送压测")
        self.item_S_T_STA_child_ota_test.setCheckState(0, Qt.Unchecked)
        self.item_S_T_STA_child_ota_test.setText(1, "")
        self.item_S_T_STA_child_ota_test.setText(2, "次")
        self.item_S_T_STA_child_ota_test.setFlags(
            self.item_S_T_STA_child_ota_test.flags() | Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEditable)


if __name__ == '__main__':
    # print(conf_path.project_path)
    subprocess.Popen(conf_path.bat_pre_info_path, shell=True, stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE).communicate(timeout=120)
    app = QtWidgets.QApplication(sys.argv)
    myshow = UIDisplay()
    myshow.show()
    app.exec_()


    #
