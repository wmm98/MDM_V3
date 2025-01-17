import allure
import configparser

from DevicePage.UIAuto2Page import UIAutoPage
from WebPage import ota_page
from Common.log import MyLog
from Common.config import Config, MDM3Interface
from WebPage.request_method import RequestMethod

log = MyLog()


class TestOTA:

    def setup_class(self):
        self.bg_conf_file = configparser.ConfigParser()
        self.bg_conf_file.read(Config.bg_config_ini_path)
        self.ui_conf_file = configparser.ConfigParser()
        self.ui_conf_file.read(Config.ui_config_ini_path)
        self.device_name = self.ui_conf_file.get(Config.section_ui_to_background,
                                            Config.ui_option_device_name)
        self.ota_page = ota_page.OTAPage()
        self.request_method = RequestMethod()
        self.device_ui_page = UIAutoPage(self.device_name)
        self.sn = self.device_ui_page.remove_special_char(self.device_ui_page.get_device_serial())

    def teardown_class(self):
        print("运行结束")

    @allure.feature("stability_normal_release_ota")
    @allure.title("压测ota正常发布")
    def test_normal_release_ota_package(self):
        # try:
        log.info("***************ota压测开始***************")
        ota_release_url = MDM3Interface.test_base_url + MDM3Interface.ota_release_url
        session_id = self.ui_conf_file.get(Config.section_ui_to_background, Config.option_session_id)
        department_id = int(self.ui_conf_file.get(Config.section_ui_to_background, Config.option_department_id))
        device_name = self.device_name
        ota_name = self.ui_conf_file.get(Config.section_ota_interface, Config.option_ota_name)
        ota_id = int(self.ui_conf_file.get(Config.section_ota_interface, Config.option_ota_id))
        is_ota_part_silent = int(self.ui_conf_file.get(Config.section_ota_interface, Config.option_ota_is_part_silent))
        is_not_ota_silent = int(self.ui_conf_file.get(Config.section_ota_interface, Config.option_ota_is_not_silent))
        if is_ota_part_silent:
            semiSilent = 1
            silentIns = True
        elif is_not_ota_silent:
            semiSilent = 0
            silentIns = False

        ota_release_json = {}
        ota_release_json["departmentId"] = department_id
        ota_release_json["id"] = ota_id
        ota_release_json["semiSilent"] = semiSilent
        ota_release_json["silentIns"] = silentIns
        ota_release_json["sn"] = self.sn
        ota_release_json["upgradeType"] = 2

        # 先检查设备是否在线

        # 释放ota
        ota_release_result = self.request_method.m_post(url=ota_release_url, json=ota_release_json, session_id=session_id).json()
        print(ota_release_result)
        if ota_release_result["code"] == 100000:
            log.info("ota发布成功")
        else:
            log.error("ota发布失败")
        # ("{'code': 63043, 'message': 'ota upgrade but has the inprocess task doing,pls del the inprocess task or retry it when the old task is end ,"
        #  "the sn is :A4B0611003033028,', 'data': None}")
        log.info("***************ota压测结束***************")
        # except Exception as e:
        #     log.error(str(e))