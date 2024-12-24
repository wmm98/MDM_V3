import os.path
import time
from http.client import responses

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

    def m_post(self, url, session_id=None, files=None, data=None, json=None, **kwargs):
        if session_id is None:
            response = requests.post(url, data=data, json=json, files=files, **kwargs)
            return response
        else:
            headers = {'Sessionid': session_id}
            response = requests.post(url, data=data, json=json, files=files, headers=headers, **kwargs)
            return response

    def m_delete(self, url, session_id, json=None, **kwargs):
        headers = {'Sessionid': session_id}
        response = requests.delete(url, json=json, headers=headers, **kwargs)
        return response

    def m_put(self, url, session_id, data=None, **kwargs):
        headers = {'Sessionid': session_id}
        response = requests.put(url, data=data, headers=headers, **kwargs)
        return response

    def split_file(self, file_path, chunk_size=10 * 1024 * 1024):
        file_number = 1
        file_parts = []
        with open(file_path, 'rb') as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                chunk_file_name = "%d_%s" % (file_number, os.path.basename(file_path))
                with open(chunk_file_name, 'wb') as chunk_file:
                    chunk_file.write(chunk)
                file_parts.append(chunk_file_name)
                file_number += 1
        return file_parts


if __name__ == '__main__':
    re = RequestMethod()
    # 获取验证码
    # response = re.m_get("http://192.168.0.30:8888/api/v1/captcha")
    # print(response.json())
    # print(response.status_code)

    # 登录
    # header = {'Content-Type': 'application/json'}
    # response = re.m_post(url="http://192.168.0.30:8888/api/v1/login", json={"username": "wumm", "password": "telpo.123", "uuid": "ygrsyiwlwwedjgvoqzehykqdnhrkphgswyme", "captcha": "3nnwy"})
    # print(response.json())

    # 上传小文件<10M
    # filename = "T10_qcm2290_sv12_fv2.0.7_pv2.0.7-9.9.9.zip"
    # file = open(filename, "rb").read()
    # print(type(file))
    # files = {'file': (filename, file, 'multipart/form-data')}
    # # 上传OTA包
    # session_id = "ef223096cd6f9e5c8692d864fe59e747"
    # form_data = {"file_name": filename, "file_size": 7129252, "block_size": 10485760, "index": 1, "total_blocks": 1,
    #              "multil_block": "ture", "filename": "T10_qcm2290_sv12_fv2.0.7_pv2.0.7-9.9.9.zip",
    #              "timestamp": 1735023182, "token": "a90295f30c130250719898ab6730d403"}
    # url = "http://192.168.0.30:8080/api/v1/upload/ota"
    # response = re.m_post(url=url, session_id=session_id, data=form_data, files=files)
    # print(response.json())

    # 上传大于10M的文件
    base_path = os.path.join(os.getcwd())
    filename = "T10_qcm2290_sv12_fv2.1.7_pv2.1.7-9.9.9.zip"
    file_path = os.path.join(base_path, "binary_", filename)
    session_id = "205cca6276f3560860d63b5429bac6fc"
    form_data = {"file_name": filename, "file_size": 34655441, "block_size": 10485760,
                 "multil_block": "true", "filename": filename,
                 "timestamp": "1735034638", "token": "dce234c0c010a558a09ff2269700c017"}
    url = "http://192.168.0.30:8080/api/v1/upload/ota"

    file_parts = re.split_file(file_path)
    # print(file_parts)
    # for file in file_parts:
    #     print(file)
    #     print(os.path.getsize(file))

    for index, part in enumerate(file_parts, start=1):
        print(index, part)
        file = open(part, "rb")
        files = {'data': (part, file.read(), 'multipart/form-data')}
        form_data['index'] = index
        form_data['total_blocks'] = len(file_parts)
        response = re.m_post(url=url, session_id=session_id, data=form_data, files=files)
        print(response.json())
        file.close()

    # file = open("3_T10_qcm2290_sv12_fv2.1.7_pv2.1.7-9.9.9.zip", "rb").read()
    # files = {'data': ("3_T10_qcm2290_sv12_fv2.1.7_pv2.1.7-9.9.9.zip", file, 'multipart/form-data')}
    # form_data['index'] = 3
    # form_data['total_blocks'] = 4
    # print("参数：")
    # for i in form_data:
    #     print(i, ":", form_data[i])
    # print("返回：")
    # response = re.m_post(url=url, session_id=session_id, data=form_data, files=files)
    # print(response.json())


