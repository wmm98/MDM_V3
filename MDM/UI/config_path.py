import os


class UIConfigPath:
    project_path = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
    # project_path = os.path.join(str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))), "Stability")
    # print(project_path)
    background_config_file_path = os.path.join(project_path, "UI", "background_config.ini")
    ui_config_file_path = os.path.join(project_path, "UI", "ui_config.ini")
    debug_log_path = os.path.join(project_path, "Log", "Debug", "log.log")
    run_bat_path = os.path.join(project_path, "main.bat")

    # 验证码路径
    captcha_path = os.path.join(project_path, "UI", "captcha.png")

    bat_pre_info_path = os.path.join(project_path, "UI", "bat_pre_info.bat")

