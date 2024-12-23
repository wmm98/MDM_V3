import requests


class RequestMethod:
    def __init__(self):
        pass

    def m_get(self, url, session_id=None, params=None, **kwargs):
        if session_id is None:
            response = requests.get(url, params=params, **kwargs)
            return response
        else:
            headers = {'Sessionid': session_id}
            response = requests.get(url, params=params, headers=headers, **kwargs)
            return response

    def m_post(self, url, session_id=None, data=None, json=None, **kwargs):
        if session_id is None:
            response = requests.post(url, data=data, json=json, **kwargs)
            return response
        else:
            headers = {'Sessionid': session_id}
            response = requests.post(url, data=data, json=json, headers=headers, **kwargs)
            return response

    def m_delete(self, url, session_id, json=None, **kwargs):
        headers = {'Sessionid': session_id}
        response = requests.delete(url, json=json, headers=headers, **kwargs)
        return response

    def m_put(self, url, session_id, data=None, **kwargs):
        headers = {'Sessionid': session_id}
        response = requests.put(url, data=data, headers=headers, **kwargs)
        return response


if __name__ == '__main__':
    re = RequestMethod()
    # 获取验证码
    # response = re.m_get("http://192.168.0.30:8888/api/v1/captcha")
    # print(response.json())
    # print(response.status_code)

    # 登录
    header = {'Content-Type': 'application/json'}
    response = re.m_post(url="http://192.168.0.30:8888/api/v1/login", json={"username": "wumm", "password": "telpo.123", "uuid": "ygrsyiwlwwedjgvoqzehykqdnhrkphgswyme", "captcha": "3nnwy"})
    print(response.json())