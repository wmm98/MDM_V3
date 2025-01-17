from WebPage.request_method import RequestMethod
from Common.public_page import PublicPage

re_method = RequestMethod()


class LoginPage(PublicPage):

    def __init__(self):
        self.session_id = None

    def get_captcha(self, url):
        response = re_method.m_get(url=url)
        return response.json()

    def login(self, url, info):
        response = re_method.m_post(url=url, json={"username": info["username"], "password": info["password"], "uuid": info["uuid"], "captcha": info["captcha"]})
        return response


if __name__ == '__main__':
    login = LoginPage()
    # 获取验证码
    # response = login.get_captcha("http://192.168.0.30:8888/api/v1/captcha")
    # uuid = response["data"]["uuid"]
    # captcha_base64 = response["data"]["captcha"]

    login_info = {"username": "wumm", "password": "telpo.123", "uuid": "gtwouclqhbbluziudnobilqlndrcdgadmhvx", "captcha": "yx7ex"}
    # 登录
    response = login.login("http://192.168.0.30:8888/api/v1/login", login_info)
    # print(response)
    result = response.json()

    for i in result:
        print(i, result[i])
    print("*************************")
    print(result["data"]["session_id"])

    department_id = result["data"]["user"]["department_id"]
    print(department_id)



