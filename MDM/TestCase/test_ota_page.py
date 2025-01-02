import allure

from WebPage import ota_page

ota_pa = ota_page.OTAPage()


class TestOTA:

    def setup_class(self):
        print("开始运行")

    def teardown_class(self):
        print("运行结束")

    @allure.feature("stability_normal_release_ota")
    @allure.title("压测ota正常发布")
    def test_normal_release_ota_package(self):
        pass
