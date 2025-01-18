import time

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
        ota_part_silent_upgrade_description = "Waiting for reboot upgrade"
        upgrade_error_description = "MdmServerErr : public msg timeout"
        ota_release_url = MDM3Interface.test_base_url + MDM3Interface.ota_release_url
        session_id = self.ui_conf_file.get(Config.section_ui_to_background, Config.option_session_id)
        department_id = int(self.ui_conf_file.get(Config.section_ui_to_background, Config.option_department_id))
        test_times = int(self.ui_conf_file.get(Config.section_ota_interface, Config.test_times))
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

        flag = 1
        while flag <= test_times:
            # 获取当前测试的sn的设备是否在线


            log.info("测试前删除当前设备的ota推送记录")
            # 获取当前sn的ota历史记录
            ota_histories_url = MDM3Interface.test_base_url + MDM3Interface.ota_release_histories_url
            histories_request_base = {"pageSize": 10, "departmentId": department_id, "order": "id", "sort": "desc"}
            histories_ids_delete = []
            for hist in range(1, 11):
                history_param = histories_request_base.copy()
                history_param["page"] = hist
                print(history_param)
                print("###################################")
                ota_history_json = self.request_method.m_get(url=ota_histories_url, session_id=session_id, params=history_param).json()
                print(ota_history_json)
                if ota_history_json["code"] == 100000:
                    if ota_history_json["data"]["total"] > 1:
                        for history in ota_history_json["data"]["otaHistorys"]:
                            if self.sn in history["sn"]:
                                if history["status"] != 2:
                                    histories_ids_delete.append(history["id"])
                    else:
                        break
                else:
                    log.error(ota_history_json["data"])
                time.sleep(1)

            print(histories_ids_delete)

            # 删除未进行中的ota
            if histories_ids_delete:
                print("")
                delete_release_url = MDM3Interface.test_base_url + MDM3Interface.ota_histories_delete_url
                delete_release_data = {"ids": histories_ids_delete}
                delete_history_result = self.request_method.m_delete(url=delete_release_url, session_id=session_id, json=delete_release_data).json()
                if delete_history_result["ceode"] == 100000:
                    log.info("删除未完成的ota成功")
                else:
                    log.error("删除未完成的ota记录失败")
                    log.error(delete_history_result["data"])
            # 设备中sdcard中的system.zip包
            self.device_ui_page.remove_file("/sdcard/system.zip")
            log.info("测试前删除设备中的system.zip包")
            print(self.device_ui_page.file_is_exist("/sdcard/system.zip"))
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

            # 在设备中点击下载
            if self.device_ui_page.element_is_exist(self.device_ui_page.content_id):
                if self.device_ui_page.get_element_text(self.device_ui_page.content_id) == self.device_ui_page.ota_download_content:
                    self.device_ui_page.click_element(self.device_ui_page.confirm_id)
                    log.info("点击下载")
                self.device_ui_page.click_element(self.device_ui_page.confirm_id)
                log.info("点击下载")



            flag += 1
            time.sleep(2)
            log.info("***************ota压测结束***************")
        # except Exception as e:
        #     log.error(str(e))