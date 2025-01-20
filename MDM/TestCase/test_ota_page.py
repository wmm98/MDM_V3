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
        # upgrade_retry_description = "Waiting for reboot upgrade"
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
        # 每10%上报
        ota_release_json["progress"] = 10

        # 获取ota包的md5值
        get_ota_list_json = {"pageSize": 10, "departmentId": department_id, "order": "id", "sort": "desc"}
        get_ota_list_url = MDM3Interface.test_base_url + MDM3Interface.ota_packages_url
        # 获取压缩包MD5值
        md5_value = ""
        for i in range(1, 10):
            ota_list_json = get_ota_list_json.copy()
            ota_list_json["page"] = i
            ota_list_result = self.request_method.m_get(url=get_ota_list_url, session_id=session_id, params=ota_list_json).json()
            if ota_list_result["code"] == 100000:
                print("*****************************")
                print(ota_list_result["data"]["otas"])
                print(type(ota_list_result["data"]["otas"]))
                print("*****************************")
                if ota_list_result["data"]["otas"] is None:
                    break
                for ota in ota_list_result["data"]["otas"]:
                    if ota["id"] == ota_id:
                        md5_value = ota["md5Sum"]
                        break

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
                            print(history)
                            if self.sn in history["sn"]:
                                if history["status"] != 2:
                                    histories_ids_delete.append(history["id"])
                    else:
                        break
                else:
                    log.error(ota_history_json["data"])
                time.sleep(1)
            print("44444444444444444444444444444444444444444")
            print(histories_ids_delete)

            # 删除未进行中的ota
            if histories_ids_delete:
                print("")
                delete_release_url = MDM3Interface.test_base_url + MDM3Interface.ota_histories_delete_url
                delete_release_data = {"ids": histories_ids_delete}
                delete_history_result = self.request_method.m_delete(url=delete_release_url, session_id=session_id, json=delete_release_data).json()
                if delete_history_result["code"] == 100000:
                    log.info("删除未完成的ota成功")
                else:
                    log.error("删除未完成的ota记录失败")
                    log.error(delete_history_result["data"])
            # 设备中sdcard中的system.zip包
            self.device_ui_page.remove_file("/sdcard/system.zip")
            log.info("测试前删除设备中的system.zip包")
            print(self.device_ui_page.file_is_exist("/sdcard/system.zip"))
            # 先检查设备是否在线

            release_time_stamp = self.device_ui_page.get_current_timestamp()
            # 释放ota
            ota_release_result = self.request_method.m_post(url=ota_release_url, json=ota_release_json, session_id=session_id).json()
            print(ota_release_result)
            if ota_release_result["code"] == 100000:
                log.info("ota发布成功")
            else:
                log.error("ota发布失败")
            # ("{'code': 63043, 'message': 'ota upgrade but has the inprocess task doing,pls del the inprocess task or retry it when the old task is end ,"
            #  "the sn is :A4B0611003033028,', 'data': None}")

            # 检查释放记录信息, 半静默下载完成标志：Waiting for reboot upgrade
            """
            status": 4,
            "failDes": "MdmServerErr : public msg timeout",
            """
            latest_history_param = histories_request_base.copy()
            latest_history_param["page"] = 1
            latest_history_json = self.request_method.m_get(url=ota_histories_url, session_id=session_id, params=latest_history_param).json()
            if latest_history_json["data"]["total"] > 1:
                if latest_history_json["data"]["otaHistorys"][0]["sn"] == self.sn:
                    if self.device_ui_page.time_to_timestamp(latest_history_json["data"]["otaHistorys"][0]["createTime"]) > release_time_stamp:
                        log.info("检查到ota推送记录")
                    else:
                        log.error("未检查到ota推送记录")
                        break
                else:
                    log.error("未检查到当前sn的ota推送记录")
                    break

            while True:
                current_history_json = self.request_method.m_get(url=ota_histories_url, session_id=session_id, params=latest_history_param).json()
                create_time = self.device_ui_page.time_to_timestamp(current_history_json["data"]["otaHistorys"][0]["createTime"])
                if latest_history_json["data"]["otaHistorys"][0]["sn"] == self.sn:
                    if create_time > release_time_stamp:
                        if current_history_json["data"]["otaHistorys"][0]["status"] == 1:
                            if "%" in current_history_json["data"]["otaHistorys"][0]["failDes"]:
                                log.info("在下载中...")

                            elif (self.device_ui_page.remove_special_char(current_history_json["data"]["otaHistorys"][0]["failDes"]).upper ==
                                  self.device_ui_page.remove_special_char(ota_part_silent_upgrade_description).upper):
                                log.info("下载完成，等待重启升级")
                                # 检查终端是否有system.zip包
                                if self.device_ui_page.file_is_exist("/sdcard/system.zip"):
                                    log.info("终端有system.zip包")
                                    if md5_value == self.device_ui_page.get_file_md5("/sdcard/system.zip"):
                                        log.info("md5值校验通过")
                                        break
                                    else:
                                        log.error("md5值校验失败")
                                        time.sleep(3)
                                        raise
                            elif (self.device_ui_page.remove_special_char(current_history_json["data"]["otaHistorys"][0]["failDes"]).upper ==
                                  self.device_ui_page.remove_special_char(upgrade_error_description).upper):
                                self.device_ui_page.reboot_device()
                                break
                        elif current_history_json["data"]["otaHistorys"][0]["status"] == 2:
                            log.info("ota升级成功")
                        else:
                            log.error("ota升级失败")
                            break
                time.sleep(1)

            # 删除system.zip包
            self.device_ui_page.remove_file("/sdcard/system.zip")
            if self.device_ui_page.file_is_exist("/sdcard/system.zip"):
                self.device_ui_page.remove_file("/sdcard/system.zip")

            # 重启，走完升级流程
            while True:
                self.device_ui_page.reboot_device()
                self.device_ui_page.restart_adb_server()
                if not self.device_ui_page.devices_adb_online():
                    break
                time.sleep(1)

            # 检查adb是否在线
            while True:
                if self.device_ui_page.devices_adb_online():
                    break
                time.sleep(1)

            # 检查设备是否再次重启升级
            while True:
                if not self.device_ui_page.devices_adb_online():
                    break
                time.sleep(1)

            # 检查设备在线情况
            while True:
                if self.device_ui_page.devices_adb_online():
                    break
                time.sleep(1)

            flag += 1
            time.sleep(2)

        log.info("***************ota压测结束***************")
        # except Exception as e:
        #     log.error(str(e))