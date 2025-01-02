import time
import requests
import os


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
    session_id = "3618d1b189447898f327c278a9bfc8a2"
    form_data = {"file_name": filename, "file_size": 34655441, "block_size": 10485760,
                 "multil_block": "true", "filename": filename,
                 "timestamp": "1735094960", "token": "4e69addd4527949ccafa263270b000ff"}
    url = "http://192.168.0.30:8080/api/v1/upload/ota"

    file_parts = re.split_file(file_path)
    # print(file_parts)
    # for file in file_parts:
    #     print(file)
    #     print(os.path.getsize(file))
    for index, part in enumerate(file_parts, start=1):
        with open(part, "rb") as file:
            files = {'data': (part, file.read(), 'multipart/form-data')}
            form_data['index'] = index
            form_data['total_blocks'] = len(file_parts)
            response = re.m_post(url=url, session_id=session_id, data=form_data, files=files)
            print(response.json())

    # 解释文件
    express_url = "http://192.168.0.30:8080/api/v1/ota/packages/upload"
    express_form_data = {"departmentId": 55,
                         "url": "http://192.168.0.32:8000/fileStatic/tmp/55/ota/T10_qcm2290_sv12_fv2.1.7_pv2.1.7-9.9.9.zip"}
    express_response = re.m_post(url=express_url, session_id=session_id, json=express_form_data)
    print(express_response.json())
    # 返回create所需要的信息

    # 更新文件
    update_url = "http://192.168.0.30:8080/api/v1/ota/packages/create"
    download_url = "http://192.168.0.32:8000/fileStatic/tmp/55/ota/T10_qcm2290_sv12_fv2.1.7_pv2.1.7-9.9.9.zip"
    update_form_data = {"departmentId": 55, "description": "", "devModel": "T10", "downloadUrl": download_url,
                        "firmwareVersion": "fv2.1.7",
                        "md5Sum": "37f283dc90c78ac50bef66efec873743",
                        "name": "T10_qcm2290_sv12_fv2.1.7_pv2.1.7-9.9.9.zip", "otaType": 0, "size": 7129252,
                        "systemVersion": "sv12",
                        "version": "pv2.1.7-9.9.9.zip", "wirelessModule": "qcm2290"}
    update_response = re.m_post(url=update_url, session_id=session_id, json=update_form_data)
    print(update_response.json())
    # 返回code 63009表示 ota包已经存在

    # 获取所有ota包列表
    print("获取列表")
    time.sleep(3)
    list_url = "http://192.168.0.30:8080/api/v1/ota/packages"
    list_data = {"page": 1, "pageSize": 10, "departmentId": 55, "order": "id", "sort": "desc"}
    list_response = re.m_get(url=list_url, session_id=session_id, params=list_data)
    print(list_response.json())

    # # 删除文件
    # delete_url = "http://192.168.0.30:8080/api/v1/ota/packages/delete"
    # delete_data = {"ids": [103], "isSiSafe": False}
    # delete_response = re.m_delete(url=delete_url, session_id=session_id, json=delete_data)
    # print(delete_response.json())

    # release ota
    # release_url = "http://192.168.0.30:8080/api/v1/ota/packages/release"
    # release_data = {"id": 104, "semiSilent": 0, "departmentId": 55, "silentIns": True, "sn": "B49T010001600008", "upgradeType":2}
    # release_response = re.m_post(url=release_url, session_id=session_id, json=release_data)
    # print(release_response.json())

    # 获取ota释放记录
    release_list_url = "http://192.168.0.30:8080/api/v1/ota/histories"
    release_list_data = {"page": 1, "pageSize": 10, "departmentId": 55, "order": "id", "sort": "desc"}
    release_list_response = re.m_get(url=release_list_url, session_id=session_id, params=release_list_data)
    print(release_list_response.json())

    # 删除ota释放记录
    delete_release_url = "http://192.168.0.30:8080/api/v1/ota/histories/delete"
    delete_release_data = {"ids": [1]}
    delete_release_response = re.m_delete(url=delete_release_url, session_id=session_id, json=delete_release_data)
    print(delete_release_response.json())
