

class HttpInterfaceConfig:
    test_login_address = "http://192.168.0.30:8888/api/v1/login"
    test_get_captcha_address = "http://192.168.0.30:8888/api/v1/captcha"
    test_get_ota_list_address = "http://192.168.0.30:8080/api/v1/ota/packages"
    test_delete_ota_address = "http://192.168.0.30:8080/api/v1/ota/packages/delete"
    test_upload_ota_address = "http://192.168.0.30:8080/api/v1/upload/ota"
    test_parse_ota_address = "http://192.168.0.30:8080/api/v1/ota/packages/upload"
    test_update_ota_address = "http://192.168.0.30:8080/api/v1/ota/packages/create"
    test_bind_devices_address = "http://192.168.0.30:8080/api/v3/device/basic/create"
    test_get_devices_address = "http://192.168.0.30:8080/api/v3/device/basic/list"

    release_login_address = "https://mdm3.telpopaas.com/api/v1/login"
    release_get_captcha_address = "https://mdm3.telpopaas.com/api/v1/captcha"
    release_bind_devices_address = "https://mdm3.telpopaas.com/api/v3/device/basic/create"
    release_get_devices_address = "https://mdm3.telpopaas.com/api/v3/device/basic/list"