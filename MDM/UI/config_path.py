import os


class UIConfigPath:
    project_path = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
    # project_path = os.path.join(str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))), "Stability")
    # print(project_path)
    background_config_file_path = os.path.join(project_path, "UI", "background_config.ini")
    ui_config_file_path = os.path.join(project_path, "UI", "ui_config.ini")
    debug_log_path = os.path.join(project_path, "Log", "Debug", "log.log")
    main_bat_path = os.path.join(project_path, "main.bat")

    # 验证码路径
    captcha_path = os.path.join(project_path, "UI", "captcha.png")

    bat_pre_info_path = os.path.join(project_path, "UI", "bat_pre_info.bat")

    # ota相关路径
    package_path = os.path.join(project_path, "Package")
    ota_path = os.path.join(package_path, "OTA")
    ota_origin_path = os.path.join(ota_path, "Original")
    ota_split_path = os.path.join(ota_path, "Split")
