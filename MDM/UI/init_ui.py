import os
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QHBoxLayout, QCheckBox, QComboBox, QButtonGroup, QWidget, QSplitter, QTextEdit
from PyQt5.QtCore import pyqtSlot, pyqtSignal
import config_path


class ClickableLabel(QtWidgets.QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)


class Ui_MainWindow(config_path.UIConfigPath):
    options = QtWidgets.QFileDialog.Options()
    options |= QtWidgets.QFileDialog.ReadOnly

    def __init__(self):
        self.stop_process_button = QtWidgets.QPushButton("停止压测")

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 700)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        # 创建水平布局
        self.main_layout = QHBoxLayout(self.centralwidget)

        # 创建 QSplitter 控件，分割两个子窗口
        splitter = QSplitter()
        self.main_layout.addWidget(splitter)

        # 左侧所有部件
        left_widget = QWidget()
        self.verticalLayout_left = QtWidgets.QVBoxLayout(left_widget)

        layout_device_info = QHBoxLayout()
        self.label_device_name = QtWidgets.QLabel("设备名称:")
        self.edit_device_name = QComboBox()
        layout_device_info.addWidget(self.label_device_name)
        layout_device_info.addWidget(self.edit_device_name)
        layout_device_info.addStretch(1)
        self.verticalLayout_left.addLayout(layout_device_info)
        self.verticalLayout_left.addWidget(QtWidgets.QLabel())

        user_info_layout = QHBoxLayout()
        self.label_user_name = QtWidgets.QLabel("用户名:")
        self.edit_user_name = QtWidgets.QLineEdit()
        self.label_password = QtWidgets.QLabel("密码:")
        self.edit_password = QtWidgets.QLineEdit()
        user_info_layout.addWidget(self.label_user_name)
        user_info_layout.addWidget(self.edit_user_name)
        user_info_layout.addWidget(self.label_password)
        user_info_layout.addWidget(self.edit_password)
        user_info_layout.addStretch(1)
        self.verticalLayout_left.addLayout(user_info_layout)
        self.verticalLayout_left.addWidget(QtWidgets.QLabel())

        layout_captcha_info = QHBoxLayout()
        self.label_captcha = QtWidgets.QLabel("验证码:")
        self.edit_captcha = QtWidgets.QLineEdit()

        # Create a QLabel to display the captcha Image
        self.captcha_button = ClickableLabel()
        self.captcha_button.setAlignment(QtCore.Qt.AlignCenter)

        self.login_tips = QtWidgets.QLabel()
        self.login_tips.setVisible(False)

        layout_captcha_info.addWidget(self.label_captcha)
        layout_captcha_info.addWidget(self.edit_captcha)
        layout_captcha_info.addWidget(self.captcha_button)
        layout_captcha_info.addWidget(self.login_tips)
        layout_captcha_info.addStretch(1)
        self.verticalLayout_left.addLayout(layout_captcha_info)
        self.verticalLayout_left.addWidget(QtWidgets.QLabel())

        login_layout = QHBoxLayout()
        self.login_button = QtWidgets.QPushButton("登录测试服")
        self.login_release_button = QtWidgets.QPushButton("登录正式服")
        login_layout.addWidget(self.login_button)
        login_layout.addWidget(self.login_release_button)
        login_layout.addStretch(1)
        self.verticalLayout_left.addLayout(login_layout)
        self.verticalLayout_left.addWidget(QtWidgets.QLabel())

        # 用例树
        self.treeWidget = QtWidgets.QTreeWidget()
        self.treeWidget.setSelectionMode(QtWidgets.QTreeWidget.ExtendedSelection)  # 设置多选模式
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.treeWidget.setFixedHeight(400)
        self.verticalLayout_left.addWidget(self.treeWidget)
        self.verticalLayout_left.addWidget(QtWidgets.QLabel())

        self.submit_button = QtWidgets.QPushButton("开始压测")
        self.verticalLayout_left.addWidget(self.submit_button)

        self.stop_process_button.setDisabled(True)
        self.verticalLayout_left.addWidget(self.stop_process_button)

        self.verticalLayout_left.addWidget(QtWidgets.QLabel())

        # 右侧部
        right_widget = QWidget()
        self.verticalLayout_right = QtWidgets.QVBoxLayout(right_widget)
        self.verticalLayout_right.addWidget(QtWidgets.QLabel("实时log打印:"))
        # 展示log
        self.text_edit = ScrollablePlainTextEdit()
        self.text_edit.setReadOnly(True)
        self.verticalLayout_right.addWidget(self.text_edit)

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setStyleSheet("""
                                    QSplitter::handle {
                                        background: #f0f0f0;  /* 分割条的颜色为最浅的灰色 */
                                        width: 1px;           /* 分割条的最细宽度 */
                                        border: 1px solid #CCCCCC; /* 分割条的边框颜色为灰白色 */
                                    }
                                    QSplitter::handle:horizontal {
                                        height: 100%;  /* 垂直分割条的高度 */
                                    }
                                    QSplitter::handle:vertical {
                                        width: 100%;   /* 水平分割条的宽度 */
                                    }
                                """)

        # 设置伸展因子确保两侧距离一致
        splitter.setStretchFactor(0, 1)  # 左侧部件的伸展因子
        splitter.setStretchFactor(1, 1)  # 右侧部件的伸展因子

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
        MainWindow.setWindowTitle(_translate("MainWindow", "压测用例配置界面"))


class ScrollablePlainTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 连接 rangeChanged 信号到 slot_scroll_to_bottom 槽
        self.verticalScrollBar().rangeChanged.connect(self.slot_scroll_to_bottom)

    @pyqtSlot(int, int)
    def slot_scroll_to_bottom(self, min, max):
        # 设置滚动条到底部
        self.verticalScrollBar().setValue(max)


