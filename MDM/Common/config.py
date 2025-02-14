import os


class Config:
    project_path = path_dir = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
    xml_report_path = os.path.join(project_path, "Report", "xml")
    html_report_path = os.path.join(project_path, "Report", "html")
    environment_properties_path = os.path.join(project_path, "Report", "environment.properties")
    debug_log_path = os.path.join(project_path, "Log", "Debug", "log.log")
    # 两个ini文件路径
    bg_config_ini_path = os.path.join(project_path, "UI", "background_config.ini")
    ui_config_ini_path = os.path.join(project_path, "UI", "ui_config.ini")

    section_ui_to_background = "UI-Background"
    section_background_to_ui = "Background-UI"

    # 公共
    ui_option_device_name = "device_name"
    bg_option_devices_name = "devices_name"
    bg_option_COM_ports = "COM_ports"
    bg_option_device_sn = "device_sn"
    ui_option_cases = "cases"
    # 是否进行失败概率性统计测试
    is_probability_test = "is_probability_test"
    # 每一轮间隔时长
    test_interval = "rounds_interval"
    # 通用模块的关到开的时长
    bt_interval = "bt_interval"
    test_times = "test_times"

    # 接口相关
    section_web_interface = "Web-Interface"
    option_session_id = "session_id"
    option_department_id = "department_id"

    section_ota_interface = "OTA"
    option_ota_name = "ota_name"
    option_ota_id = "ota_id"
    option_ota_is_part_silent = "ota_part_silent"
    option_ota_is_not_silent = "ota_not_silent"

    section_apk_silent_upgrade = "APK_Single_Stability"
    option_apk_package_name = "apk_package_name"
    option_apk_id = "apk_id"


class MDM3Interface:
    test_base_url = "http://192.168.0.30:8080/"
    release_base_url = "https://mdm3.telpopaas.com/"

    ota_release_url = "api/v1/ota/packages/release"
    ota_release_histories_url = "api/v1/ota/histories"
    ota_histories_delete_url = "api/v1/ota/histories/delete"
    ota_packages_url = "api/v1/ota/packages"
    devices_list_url = "api/v3/device/basic/list"



