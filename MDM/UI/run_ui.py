import subprocess
import sys
import base64
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtCore import QProcess, Qt, pyqtSlot
from PyQt5.QtGui import QTextDocument, QTextCursor, QTextImageFormat
from init_ui import Ui_MainWindow
from PyQt5.QtCore import QByteArray
from PyQt5.QtGui import QPixmap
import os
import requests
import configfile
import config_path

conf_path = config_path.UIConfigPath()


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

        self.bg_config = configfile.ConfigP(self.background_config_file_path)
        self.ui_config = configfile.ConfigP(self.ui_config_file_path)

        self.setupUi(self)
        self.AllTestCase = None
        self.inti_ui()
        self.init_signal_slot()
        self.cases_selected_sum = 0
        self.uuid = None

    def inti_ui(self):
        # 初始化
        # 初始化图片cursor
        # self.cursor = QTextCursor(self.document)
        # self.cursor_camera = QTextCursor(self.document_camera)

        self.ui_config.init_config_file()
        self.ui_config.add_config_section(self.ui_config.section_ui_to_background)

        # self.ui_config.init_config_file()
        # self.ui_config.add_config_section(self.ui_config.section_ui_to_background)
        # 初始化进程
        self.qt_process = QProcess()
        self.submit_button.clicked.connect(self.handle_submit)
        # 初始化图片cursor
        # self.cursor = QTextCursor(self.document)

        # 展示用例树
        self.list_tree_cases()
        self.select_devices_name()

    def init_signal_slot(self):

        self.treeWidget.expandAll()
        self.treeWidget.itemChanged.connect(self.handlechanged)
        # 用例树点击事件
        # self.treeWidget.itemClicked.connect(self.on_item_clicked)

        self.captcha_button.clicked.connect(self.display_captcha)
        self.login_button.clicked.connect(self.login)

        self.qt_process.readyReadStandardOutput.connect(self.handle_stdout)
        self.qt_process.readyReadStandardError.connect(self.handle_stderr)

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
        url = "http://192.168.0.30:8888/api/v1/login"
        json_data = {"username": username, "password": password, "uuid": self.uuid, "captcha": captcha}
        response = requests.post(url=url, json=json_data).json()
        if response["code"] == 100000:
            print(response["data"])
            session_id = response["data"]["session_id"]
            department_id = str(response["data"]["user"]["departmentId"])
            self.ui_config.add_config_option(self.ui_config.section_ui_to_background, self.ui_config.option_session_id, session_id)
            self.ui_config.add_config_option(self.ui_config.section_ui_to_background, self.ui_config.option_department_id, department_id)
            self.login_tips.setVisible(True)
            self.login_tips.setText("登录成功！")
            self.login_tips.setStyleSheet("color:red")
            self.get_information("登录成功!")
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

    def get_captcha(self):
        # 获取验证码
        response = requests.get(url="http://192.168.0.30:8888/api/v1/captcha").json()
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

    @pyqtSlot()
    def handle_stdout(self):
        data = self.qt_process.readAllStandardOutput()
        stdout = bytes(data).decode("utf-8")
        print("Stdout:", stdout)

    @pyqtSlot()
    def handle_stderr(self):
        data = self.qt_process.readAllStandardError()
        stderr = bytes(data).decode("utf-8")
        print("Stderr:", stderr)

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
            if "ota推送--正常压测" in case:
                self.transfer_cases.append("stability_normal_release_ota")

        self.ui_config.add_config_option(self.ui_config.section_ui_to_background,
                                         self.ui_config.ui_option_device_name,
                                         self.edit_device_name.currentText())
        # 保存用例
        self.ui_config.add_config_option(self.ui_config.section_ui_to_background,
                                         self.ui_config.ui_option_cases, ",".join(self.transfer_cases))


        # try:
        project_path = os.path.dirname(os.path.abspath(__file__))

        base_path = getattr(sys, '_MEIPASS', os.path.abspath(""))
        # script_path = os.path.join(base_path, "main.py")

        if getattr(sys, 'frozen', False):
            # 打包后的 .exe
            meipass_path = getattr(sys, '_MEIPASS', os.path.abspath(""))
            python_path = os.path.join(meipass_path, "python.exe")
            main_py_path = os.path.join(meipass_path, "main.py")
            print("打包后的 .exe")
        else:
            # 开发环境
            python_path = sys.executable
            main_py_path = os.path.join(os.path.dirname(__file__), "main.py")
            print(main_py_path)

        self.start_qprocess(python_path, main_py_path)
            #
            # # 连接输出和错误信号以捕获输出日志
            # self.qt_process.readyReadStandardOutput.connect(self.handle_stdout)
            # self.qt_process.readyReadStandardError.connect(self.handle_stderr)

            # self.stop_process_button.setEnabled(True)
            # self.submit_button.setDisabled(True)
            # self.submit_button.setText("测试中...")
        # except Exception as e:
            # print(e)

    def start_subprocess(self):
        if getattr(sys, 'frozen', False):
            # 打包后的 .exe
            meipass_path = getattr(sys, '_MEIPASS', os.path.abspath(""))
            python_path = os.path.join(meipass_path, "python.exe")
            main_py_path = os.path.join(meipass_path, "main.py")
        else:
            # 开发环境
            python_path = sys.executable
            main_py_path = os.path.join(os.path.dirname(__file__), "main.py")

        # 启动新进程
        subprocess.Popen([python_path, main_py_path])

    # 或者使用 QProcess
    def start_qprocess(self, python_path, main_py_path):
        # 启动新进程
        self.qt_process.start(python_path, [main_py_path])

    def stop_process(self):
        # 文件位置初始化
        self.force_task_kill()
        self.stop_process_button.setDisabled(True)
        self.submit_button.setEnabled(True)
        self.submit_button.setText("开始测试")

    def start_qt_process(self, file_path):
        # 启动 外部 脚本
        python_executable = sys.executable  # 获取当前 Python 环境的路径
        self.qt_process.start(python_executable, [file_path])  # 启动外部脚本
        # Wait for the process to start
        if not self.qt_process.waitForStarted():
            print("启动失败")
        else:
            print("启动成功")

    def handle_stdout(self):
        output = self.qt_process.readAllStandardOutput().data().decode()
        print("STDOUT:", output)

    def handle_stderr(self):
        error = self.qt_process.readAllStandardError().data().decode()
        print("STDERR:", error)

    def force_task_kill(self):
        self.qt_process.startDetached("taskkill /PID %s /F /T" % str(self.qt_process.processId()))

    def closeEvent(self, event):
        # 在窗口关闭时停止定时器,关闭任务运行
        # 停止 QProcess 进程
        self.qt_process.startDetached("taskkill /PID %s /F /T" % str(self.qt_process.processId()))
        event.accept()

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
        # 我添加的
        for i in range(tree_item.childCount()):
            child_item = tree_item.child(i)
            result["children"].append(self.get_tree_item_status(child_item))
        return result

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
        self.item_S_T_STA_child_boot_check = QTreeWidgetItem(self.item_S_T_STA)
        self.item_S_T_STA_child_boot_check.setText(0, "ota推送--正常压测")
        self.item_S_T_STA_child_boot_check.setCheckState(0, Qt.Unchecked)
        self.item_S_T_STA_child_boot_check.setText(1, "")
        self.item_S_T_STA_child_boot_check.setText(2, "次")
        self.item_S_T_STA_child_boot_check.setFlags(
            self.item_S_T_STA_child_boot_check.flags() | Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEditable)


if __name__ == '__main__':
    # print(conf_path.project_path)
    subprocess.Popen(conf_path.bat_pre_info_path, shell=True, stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE).communicate(timeout=120)
    app = QtWidgets.QApplication(sys.argv)
    myshow = UIDisplay()
    myshow.display_captcha()
    myshow.show()
    app.exec_()
