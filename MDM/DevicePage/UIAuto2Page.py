from DevicePage.AndroidDevicePage import DevicePage


class UIAutoPage(DevicePage):
    def __init__(self, device_name):
        DevicePage.__init__(self, device_name)
        self.device_name = device_name