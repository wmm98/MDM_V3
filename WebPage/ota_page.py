from request_method import RequestMethod
import os

re_method = RequestMethod()


class OTAPage:
    def __init__(self):
        self.session_id = None

    def get_ota_list(self, url):
        response = re_method.m_get(url=url, session_id=self.session_id)
        return response.json()

    def add_ota(self, url, session_id=None, file_path=None, data=None):
        # 判断文件大于10M的就分割，少于等一一片
        if file_path:
            file_size = os.path.getsize(file_path)
            if file_size <= 10 * 1024 * 1024:
                with open(file_path, 'rb') as file:
                    files = {'data': (file_path, file.read(), 'multipart/form-data')}
                    data['index'] = 1
                    data['total_blocks'] = 1

            with open(file_path, 'rb') as file:
                files = {'data': (file_path, file, 'multipart/form-data')}
        response = re_method.m_post(url=url, data=data, files=files, session_id=session_id)


        response = re_method.m_post(url=url, data=data, files=files, session_id=session_id)
        return response

    def delete_ota(self, url, info):
        response = re_method.m_delete(url=url, json=info)
        return response

    def update_ota(self, url, info):
        response = re_method.m_put(url=url, json=info)
        return response

    def get_ota_release_list(self, url):
        response = re_method.m_get(url=url)
        return response.json()

    def delete_ota_release(self, url, info):
        response = re_method.m_delete(url=url, json=info)
        return response

if __name__ == '__main__':
    otapage = OTAPage()

