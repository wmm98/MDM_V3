import os


class Config:
    project_path = path_dir = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
    xml_report_path = os.path.join(project_path, "Report", "xml")
    html_report_path = os.path.join(project_path, "Report", "html")
    environment_properties_path = os.path.join(project_path, "Report", "environment.properties")
    debug_log_path = os.path.join(project_path, "Log", "Debug", "log.log")

    # ini�ֶ�����

    section_ui_to_background = "UI-Background"
    section_background_to_ui = "Background-UI"

    # ����
    ui_option_device_name = "device_name"
    bg_option_devices_name = "devices_name"
    bg_option_COM_ports = "COM_ports"
    ui_option_cases = "cases"
    # �Ƿ����ʧ�ܸ�����ͳ�Ʋ���
    is_probability_test = "is_probability_test"
    # ÿһ�ּ��ʱ��
    test_interval = "rounds_interval"
    # ͨ��ģ��Ĺص�����ʱ��
    bt_interval = "bt_interval"

    # �ӿ����
    section_web_interface = "Web-Interface"
    option_session_id = "session_id"
    option_department_id = "department_id"

    section_ota_interface = "OTA"
    option_ota_name = "ota_name"
    option_ota_id = "ota_id"
    option_ota_is_part_silent = "ota_part_silent"
    option_ota_is_not_silent = "ota_not_silent"