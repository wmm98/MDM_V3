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
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(Config.bg_config_ini_path)
        print(Config.ui_config_ini_path)
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
        try:
            log.info("***************ota压测开始***************")
            ota_part_silent_upgrade_description = self.device_ui_page.remove_special_char("Waiting for reboot upgrade")
            # upgrade_retry_description = "Waiting for reboot upgrade"
            upgrade_error_description = self.device_ui_page.remove_special_char("MdmServerErr : public msg timeout")
            ota_release_url = MDM3Interface.test_base_url + MDM3Interface.ota_release_url
            session_id = self.ui_conf_file.get(Config.section_ui_to_background, Config.option_session_id)
            department_id = int(self.ui_conf_file.get(Config.section_ui_to_background, Config.option_department_id))
            test_times = int(self.ui_conf_file.get(Config.section_ota_interface, Config.test_times))
            is_probability_test = int(self.ui_conf_file.get(Config.section_ota_interface, Config.is_probability_test))
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
            probability_flag = 0
            ota_release_json = {}
            ota_release_json["departmentId"] = department_id
            ota_release_json["id"] = ota_id
            ota_release_json["semiSilent"] = semiSilent
            ota_release_json["silentIns"] = silentIns
            ota_release_json["sn"] = self.sn
            ota_release_json["upgradeType"] = 2
            # 每10%上报
            ota_release_json["progress"] = 10

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
                    ota_history_json = self.request_method.m_get(url=ota_histories_url, session_id=session_id, params=history_param).json()
                    print(ota_history_json)
                    if ota_history_json["code"] == 100000:
                        if ota_history_json["data"]["otaHistorys"]:
                            for history in ota_history_json["data"]["otaHistorys"]:
                                if self.sn in history["sn"]:
                                    histories_ids_delete.append(history["id"])
                                    # if history["status"] != 2:
                                    #     histories_ids_delete.append(history["id"])
                        else:
                            break
                    else:
                        log.error("%s， 请重新登陆" % ota_history_json["message"])
                        raise
                    time.sleep(1)

                # 删除未进行中的ota
                if histories_ids_delete:
                    delete_release_url = MDM3Interface.test_base_url + MDM3Interface.ota_histories_delete_url
                    delete_release_data = {"ids": histories_ids_delete}
                    delete_history_result = self.request_method.m_delete(url=delete_release_url, session_id=session_id, json=delete_release_data).json()
                    if delete_history_result["code"] == 100000:
                        log.info("删除该设备的历史推送记录")
                    else:
                        log.error("删除未完成的ota记录失败")
                        log.error(delete_history_result["data"])
                # 设备中sdcard中的system.zip包
                self.device_ui_page.remove_file("/sdcard/system.zip")
                log.info("测试前删除设备中的system.zip包")

                # 获取ota包的md5值
                get_ota_list_json = {"pageSize": 10, "departmentId": department_id, "order": "id", "sort": "desc"}
                get_ota_list_url = MDM3Interface.test_base_url + MDM3Interface.ota_packages_url
                # 获取压缩包MD5值
                md5_value = ""
                for i in range(1, 10):
                    ota_list_json = get_ota_list_json.copy()
                    ota_list_json["page"] = i
                    ota_list_result = self.request_method.m_get(url=get_ota_list_url, session_id=session_id,
                                                                params=ota_list_json).json()
                    if ota_list_result["code"] == 100000:
                        if ota_list_result["data"]["otas"] is None:
                            break
                        for ota in ota_list_result["data"]["otas"]:
                            if ota["id"] == ota_id:
                                md5_value = ota["md5Sum"]
                                break
                # 先检查设备是否在线
                release_time_stamp = self.device_ui_page.get_current_timestamp()
                time.sleep(3)
                # # 释放ota
                ota_release_result = self.request_method.m_post(url=ota_release_url, json=ota_release_json, session_id=session_id).json()
                if ota_release_result["code"] == 100000:
                    log.info("ota发布成功")
                else:
                    log.error("ota发布失败")
                    continue
                # ("{'code': 63043, 'message': 'ota upgrade but has the inprocess task doing,pls del the inprocess task or retry it when the old task is end ,"
                #  "the sn is :A4B0611003033028,', 'data': None}")

                # 检查释放记录信息, 半静默下载完成标志：Waiting for reboot upgrade
                """
                status": 4,
                "failDes": "MdmServerErr : public msg timeout",
                """
                now_time = self.device_ui_page.get_current_time()
                latest_history_param = histories_request_base.copy()
                latest_history_param["page"] = 1
                history_flag = 0
                log.info("检查ota推送记录")
                while self.device_ui_page.get_current_time() < now_time + 60:
                    latest_history_json = self.request_method.m_get(url=ota_histories_url, session_id=session_id, params=latest_history_param).json()
                    print(latest_history_json)
                    if latest_history_json["data"]["otaHistorys"]:
                        if self.sn in latest_history_json["data"]["otaHistorys"][0]["sn"]:
                            web_create_time = self.device_ui_page.time_to_timestamp(latest_history_json["data"]["otaHistorys"][0]["createTime"])
                            if web_create_time > release_time_stamp:
                                log.info("检查到ota推送记录")
                                break
                            else:
                                history_flag += 1
                    time.sleep(1)

                if history_flag > 0:
                    log.error("未检查到ota推送记录")
                    raise

                log.info("检查ota包实时下载情况")
                while True:
                    current_history_json = self.request_method.m_get(url=ota_histories_url, session_id=session_id, params=latest_history_param).json()
                    print(current_history_json)
                    create_time = self.device_ui_page.time_to_timestamp(current_history_json["data"]["otaHistorys"][0]["createTime"])
                    if current_history_json["data"]["otaHistorys"][0]["sn"] == self.sn:
                        if create_time > release_time_stamp:
                            if current_history_json["data"]["otaHistorys"][0]["status"] == 1:
                                if "%" in current_history_json["data"]["otaHistorys"][0]["failDes"]:
                                    log.info("在下载中...")
                                    log.info("设备%s下载%s进度的为：%s" % (self.sn, current_history_json["data"]["otaHistorys"][0]["name"], current_history_json["data"]["otaHistorys"][0]["failDes"]))

                                elif self.device_ui_page.remove_special_char(current_history_json["data"]["otaHistorys"][0]["failDes"]).upper() == ota_part_silent_upgrade_description.upper():
                                    log.info("设备%s当前下载详情：%s" % (self.sn, current_history_json["data"]["otaHistorys"][0]["failDes"]))
                                    log.info("下载完成，等待重启升级")
                                    # 检查终端是否有system.zip包
                                    if self.device_ui_page.file_is_exist("/sdcard/system.zip"):
                                        log.info("终端有system.zip包")
                                        log.info("原ota包的md5值为：%s" % md5_value)
                                        system_zip_md5 = self.device_ui_page.get_file_md5("/sdcard/system.zip")
                                        log.info("终端的检测到的system.zip包md5值为：%s" % system_zip_md5)
                                        if md5_value == self.device_ui_page.get_file_md5("/sdcard/system.zip"):
                                            log.info("md5值校验通过")
                                            break
                                        else:
                                            log.error("md5值校验失败")
                                            if is_probability_test:
                                                probability_flag += 1
                                                break
                                            time.sleep(3)
                                            raise
                                else:
                                    log.info("设备%s当前详情：%s" % (self.sn, current_history_json["data"]["otaHistorys"][0]["failDes"]))
                                # elif (self.device_ui_page.remove_special_char(current_history_json["data"]["otaHistorys"][0]["failDes"]).upper() ==
                                #       self.device_ui_page.remove_special_char(upgrade_error_description).upper()):
                                #     self.device_ui_page.reboot_device()
                                #     break

                            elif current_history_json["data"]["otaHistorys"][0]["status"] == 2:
                                log.info("设备%s当前详情：%s" % (self.sn, current_history_json["data"]["otaHistorys"][0]["failDes"]))
                                log.info("ota升级成功")
                                break
                            elif current_history_json["data"]["otaHistorys"][0]["status"] == 3:
                                log.info("设备%s当前详情：%s" % (self.sn, current_history_json["data"]["otaHistorys"][0]["failDes"]))
                                log.error("ota升级失败")
                                time.sleep(3)
                                break
                            elif current_history_json["data"]["otaHistorys"][0]["status"] == 4:
                                if self.device_ui_page.remove_special_char(current_history_json["data"]["otaHistorys"][0]["failDes"]).upper() == upgrade_error_description.upper():
                                    log.info("设备%s当前详情：%s" % (self.sn, current_history_json["data"]["otaHistorys"][0]["failDes"]))
                                    log.info("重启设备")
                                    while True:
                                        self.device_ui_page.reboot_device()
                                        self.device_ui_page.restart_adb_server()
                                        if not self.device_ui_page.devices_adb_online():
                                            log.info("设备重启，检测到设备ADB不在线")
                                            break
                                        time.sleep(1)

                                    # 检查adb是否在线
                                    log.info("检测设备ADB是否在线")
                                    while True:
                                        if self.device_ui_page.devices_adb_online():
                                            log.info("设备重启成功，ADB在线")
                                            break
                                        time.sleep(1)

                                    # 检查设备是否再次重启升级
                                    log.info("检测设备是否再次升级")
                                    now_time = self.device_ui_page.get_current_time()
                                    while self.device_ui_page.get_current_time() < now_time + 90:
                                        if not self.device_ui_page.devices_adb_online():
                                            log.info("假升级中...")
                                            break
                                        time.sleep(1)

                                    # 检查设备在线情况
                                    log.info("检测设备ADB是否在线")
                                    while True:
                                        if self.device_ui_page.devices_adb_online():
                                            log.info("设备ADB在线")
                                            break
                                        time.sleep(1)
                    time.sleep(5)

                log.info("测试后的清除")
                # 删除system.zip包
                self.device_ui_page.remove_file("/sdcard/system.zip")
                if self.device_ui_page.file_is_exist("/sdcard/system.zip"):
                    self.device_ui_page.remove_file("/sdcard/system.zip")
                log.info("删除设备中的system.zip包")

                # 重启，走完升级流程
                log.info("重启设备")
                while True:
                    self.device_ui_page.reboot_device()
                    self.device_ui_page.restart_adb_server()
                    if not self.device_ui_page.devices_adb_online():
                        log.info("设备重启，检测到设备ADB不在线")
                        break
                    time.sleep(1)

                # 检查adb是否在线
                log.info("检测设备ADB是否在线")
                while True:
                    if self.device_ui_page.devices_adb_online():
                        log.info("设备ADB在线")
                        break
                    time.sleep(1)

                # if not self.device_ui_page.is_screen_on():
                #     self.device_ui_page.press_power_button()
                # time.sleep(1)
                # self.device_ui_page.unlock()
                # time.sleep(1)
                # self.device_ui_page.back_home()

                # 检查设备是否再次重启升级
                log.info("检测设备是否再次升级")
                now_time = self.device_ui_page.get_current_time()
                while self.device_ui_page.get_current_time() < now_time + 90:
                    if not self.device_ui_page.devices_adb_online():
                        log.info("假升级中...")
                        break
                    time.sleep(1)

                # 检查设备在线情况
                while True:
                    if self.device_ui_page.devices_adb_online():
                        break
                    time.sleep(1)

                log.info("第%s次ota压测完成" % flag)
                flag += 1
                time.sleep(2)
            if probability_flag > 0:
                log.info("测试总次数为：%s" % test_times)
                log.error("测试失败次数为：%s" % probability_flag)
                log.info("测试失败率为：%s" % (probability_flag / test_times))
            log.info("***************ota压测结束***************")
        except Exception as e:
            log.info("运行过程中代码异常，请检查！！")
            log.error(str(e))
            time.sleep(2)