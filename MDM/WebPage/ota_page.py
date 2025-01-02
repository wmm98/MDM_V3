import os
from MDM.WebPage.request_method import RequestMethod
from MDM.WebPage.login_page import LoginPage


re_method = RequestMethod()


class OTAPage(LoginPage):
    def __init__(self):
        self.session_id = None

    def get_ota_list(self, url, params):
        response = re_method.m_get(url=url, params=params["data"], session_id=params["session_id"])
        return response.json()

    def add_ota(self, ota_info):
        # 判断文件大于10M的就分割，少于直接上传
        # url, session_id = None, file_path = None, data = None, new_dir = None
        """
        :param ota_info: url, session_id, file_path, data, new_dir
            url:  接口地址
            file_path: 文件路径
            data: 上传文件de json数据
            new_dir: 分割文件存放路径

        :return: [response]
        """
        if ota_info['file_path']:
            file_size = os.path.getsize(ota_info['file_path'])
            if file_size <= 10 * 1024 * 1024:
                with open(ota_info['file_path'], 'rb') as file:
                    ota_info['data']['index'] = 1
                    ota_info['data']['total_blocks'] = 1
                    files = {'data': (ota_info['file_path'], file.read(), 'multipart/form-data')}
                    response = re_method.m_post(url=ota_info["url"], data=ota_info['data'], files=files,
                                                session_id=ota_info['session_id'])
                    return [response]
            else:
                responses_list = []
                file_parts = self.split_file(ota_info['file_path'], ota_info['new_dir'])
                ota_info['data']['total_blocks'] = len(file_parts)
                for i in range(len(file_parts)):
                    with open(file_parts[i], 'rb') as file:
                        ota_info['data']['index'] = i + 1
                        file = {'data': (file_parts[i], file.read(), 'multipart/form-data')}
                        response = re_method.m_post(url=ota_info["url"], data=ota_info['data'], files=file,
                                                    session_id=ota_info['session_id'])
                        responses_list.append(response.json())
                return responses_list

    def delete_ota(self, url, info):
        response = re_method.m_delete(url=url, json=info["dta"], session_id=info["session_id"])
        return response

    def update_ota(self, url, info):
        response = re_method.m_post(url=url, json=info["data"], session_id=info["session_id"])
        return response

    def create_ota(self, url, info):
        response = re_method.m_post(url=url, json=info["data"], session_id=info["session_id"])
        return response

    def release_ota(self, url, info):
        response = re_method.m_post(url=url, json=info["data"], session_id=info["session_id"])
        return response

    def get_ota_release_list(self, url, params):
        response = re_method.m_get(url=url, params=params["data"], session_id=params["session_id"])
        return response.json()

    def delete_ota_release(self, url, info):
        response = re_method.m_delete(url=url, json=info["data"], session_id=info["session_id"])
        return response


if __name__ == '__main__':
    ota = OTAPage()
    base_path = os.path.dirname(os.getcwd())
    print(base_path)

    # add ota
    ota_info = {}
    session_id = "b58709b8c79df2864962311b3c418479"
    file_name = "T10_qcm2290_sv12_fv2.1.7_pv2.1.7-9.9.9.zip"
    orig_file_path = os.path.join(base_path, "Package\\OTA\\Original", file_name)
    json_data = {"file_name": file_name, "file_size": 34655441, "block_size": 10485760,
                 "multil_block": "true", "filename": file_name,
                 "timestamp": "1735202019", "token": "6b7e81eb910d9184854391569c69d7c5"}
    new_dir = os.path.join(base_path, "Package\\OTA\\Split")
    ota_info['url'] = "http://192.168.0.30:8080/api/v1/upload/ota"
    ota_info['session_id'] = session_id
    ota_info['file_path'] = orig_file_path
    ota_info['data'] = json_data
    ota_info['new_dir'] = new_dir

    # result = ota.add_ota(ota_info)
    # print(result)
    #
    # # upload ota
    # upload_url = "http://192.168.0.30:8080/api/v1/ota/packages/upload"
    # download_url = result[-1]['data']['destination']
    # upload_data = {"departmentId": 55, "url": download_url}
    # upload_json = {"session_id": session_id, "data": upload_data}
    # upload_response = ota.create_ota(upload_url, upload_json).json()
    # print(upload_response)
    #
    # # update ota
    # update_url = "http://192.168.0.30:8080/api/v1/ota/packages/create"
    # update_data = {"departmentId": 55, "description": "", "devModel": upload_response["data"]["devModel"],
    #                "downloadUrl": download_url,
    #                "firmwareVersion": upload_response["data"]["firmwareVersion"],
    #                "md5Sum": upload_response["data"]["md5Sum"],
    #                "name": upload_response["data"]["name"], "otaType": 0, "size": upload_response["data"]["size"],
    #                "systemVersion": upload_response["data"]["systemVersion"], "version": upload_response["data"]["version"],
    #                "wirelessModule": upload_response["data"]["wirelessModule"]}
    # upload_json = {"session_id": session_id, "data": update_data}
    # update_response = ota.update_ota(update_url, upload_json)
    # print(update_response.json())

    # get ota list
    get_ota_list_url = "http://192.168.0.30:8080/api/v1/ota/packages"
    get_ota_list_data = {"departmentId": 55, "page": 1, "pageSize": 10, "order": "id", "sort": "desc"}
    get_ota_list_json = {"session_id": session_id, "data": get_ota_list_data}
    get_ota_list_response = ota.get_ota_list(get_ota_list_url, get_ota_list_json)
    print(get_ota_list_response)

    # release ota
    release_url = "http://192.168.0.30:8080/api/v1/ota/packages/release"
    release_data = {"departmentId": 55, "id": get_ota_list_response["data"]["otas"][0]["id"], "semiSilent": 0, "silentIns": True, "sn": "B49T010001600008", "upgradeType": 2}
    release_json = {"session_id": session_id, "data": release_data}
    release_response = ota.release_ota(release_url, release_json).json()
    print(release_response)
