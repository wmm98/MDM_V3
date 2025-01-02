import configparser
from config_path import UIConfigPath


class ConfigP(UIConfigPath):
    section_ui_to_background = "UI-Background"
    section_background_to_ui = "Background-UI"

    # 接口相关
    section_web_interface = "Web-Interface"
    option_session_id = "session_id"

    # 公共
    ui_option_device_name = "device_name"
    bg_option_devices_name = "devices_name"
    bg_option_COM_ports = "COM_ports"
    # 是否进行失败概率性统计测试
    is_probability_test = "is_probability_test"
    # 每一轮间隔时长
    test_interval = "rounds_interval"
    # 通用模块的关到开的时长
    bt_interval = "bt_interval"

    def __init__(self, ini_path):
        self.ini_path = ini_path
        self.config = configparser.ConfigParser()

    def init_config_file(self):
        with open(self.ini_path, 'w') as configfile:
            self.config.write(configfile)

    def add_config_section(self, section):
        self.config.read(self.ini_path)
        if section not in self.config:
            self.config.add_section(section)
        with open(self.ini_path, 'w') as configfile:
            self.config.write(configfile)

    def add_config_option(self, section, option, value):
        self.config.read(self.ini_path)
        self.add_config_section(section)
        self.config.set(section, option, value)
        with open(self.ini_path, 'w') as configfile:
            self.config.write(configfile)

    def get_option_value(self, section, option):
        self.config.read(self.ini_path)
        return self.config.get(section, option)
