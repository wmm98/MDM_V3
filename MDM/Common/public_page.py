import os
import time
from datetime import datetime

class PublicPage:
    def __init__(self):
        pass

    def split_file(self, file_path, new_dir, chunk_size=10 * 1024 * 1024):
        file_number = 1
        file_parts = []
        with open(file_path, 'rb') as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                file_name = os.path.basename(file_path)
                base, ext = os.path.splitext(file_name)
                chunk_file_name = os.path.join(new_dir, "%s_%d%s" % (base, file_number, ext))
                with open(chunk_file_name, 'wb') as chunk_file:
                    chunk_file.write(chunk)
                file_parts.append(chunk_file_name)
                file_number += 1
        return file_parts

    def remove_special_char(self, string):
        return string.replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "")

    def time_to_timestamp(self, time_str):
        time_format = "%Y-%m-%d %H:%M:%S"
        dt_object = datetime.strptime(time_str, time_format)
        timestamp = int(dt_object.timestamp())
        return timestamp

        # 获取当前的时间戳，精确到s
    def get_current_timestamp(self):
        return int(time.time())

    def get_current_time(self):
        return time.time()


if __name__ == '__main__':
    public = PublicPage()
    base_path = os.path.join(os.getcwd())
    print(base_path)
    filename = "../Package/OTA/Original/T10_qcm2290_sv12_fv2.1.7_pv2.1.7-9.9.9.zip"
    file_path = os.path.join(base_path, filename)
    new_dir = os.path.join(base_path, "binary_")
    list_parts = public.split_file(file_path, new_dir)
    print(list_parts)
