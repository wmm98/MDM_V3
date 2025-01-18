import uiautomator2 as u2
from DevicePage.AndroidDevicePage import DevicePage

omc_package_name = "com.telpo.omcservice"


class UIAutoPage(DevicePage):

    ota_download_content = "New firmware detected, whether to download?"
    ota_upgrade_content = "New firmware downloaded, whether to update?"
    content_id = "%s:id/dialog_tv_content" % omc_package_name
    confirm_id = "%s:id/dialog_btn_right" % omc_package_name
    cancel_id = "%s:id/dialog_btn_left" % omc_package_name

    def __init__(self, device_name):
        DevicePage.__init__(self, device_name)
        self.device_name = device_name
        self.device = None

    def u2_connect_device(self):
        device = u2.connect(self.device_name)
        self.device = device

    def element_is_exist(self, element_id, timeout=30):
        return self.device(resourceId=element_id).exists(timeout=timeout)

    def element_is_not_exist(self, element_id, timeout=10):
        return self.device(resourceId=element_id).wait_gone(timeout=timeout)

    def click_element(self, element_id):
        self.device(resourceId=element_id).click()

    def get_element_text(self, element_id):
        return self.device(resourceId=element_id).get_text()
