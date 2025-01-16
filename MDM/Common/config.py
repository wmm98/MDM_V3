import os


class Config:
    project_path = path_dir = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
    xml_report_path = os.path.join(project_path, "Report", "xml")
    html_report_path = os.path.join(project_path, "Report", "html")
    environment_properties_path = os.path.join(project_path, "Report", "environment.properties")
    debug_log_path = os.path.join(project_path, "Log", "Debug", "log.log")

    # ini字段属性

    section_ui_to_background = "UI-Background"
    section_background_to_ui = "Background-UI"

    # 公共
    ui_option_device_name = "device_name"
    bg_option_devices_name = "devices_name"
    bg_option_COM_ports = "COM_ports"
    ui_option_cases = "cases"
    # 是否进行失败概率性统计测试
    is_probability_test = "is_probability_test"
    # 每一轮间隔时长
    test_interval = "rounds_interval"
    # 通用模块的关到开的时长
    bt_interval = "bt_interval"

    # 接口相关
    section_web_interface = "Web-Interface"
    option_session_id = "session_id"
    option_department_id = "department_id"

    section_ota_interface = "OTA"
    option_ota_name = "ota_name"
    option_ota_id = "ota_id"
    option_ota_is_part_silent = "ota_part_silent"
    option_ota_is_not_silent = "ota_not_silent"