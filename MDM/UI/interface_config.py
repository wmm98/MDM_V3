

class HttpInterfaceConfig:
    test_login_address = "http://192.168.0.30:8888/api/v1/login"
    test_get_captcha_address = "http://192.168.0.30:8888/api/v1/captcha"
    test_get_ota_list_address = "http://192.168.0.30:8080/api/v1/ota/packages"
    test_delete_ota_address = "http://192.168.0.30:8080/api/v1/ota/packages/delete"
    test_upload_ota_address = "http://192.168.0.30:8080/api/v1/upload/ota"
    test_parse_ota_address = "http://192.168.0.30:8080/api/v1/ota/packages/upload"
    test_update_ota_address = "http://192.168.0.30:8080/api/v1/ota/packages/create"

    release_login_address = "https://mdm3.telpopaas.com/api/v1/login"
    release_get_captcha_address = "https://mdm3.telpopaas.com/api/v1/captcha"