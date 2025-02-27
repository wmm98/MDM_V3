import subprocess
from Common.log import MyLog
#
log = MyLog()


class Shell:
    @staticmethod
    def invoke(cmd, runtime=10):
        try:
            output, errors = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE).communicate(timeout=runtime)
            # output, errors = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
            #                                   stderr=subprocess.PIPE,
            #                                   creationflags=subprocess.CREATE_NO_WINDOW).communicate(timeout=runtime)
            o = output.decode("utf-8")
            return o
        except subprocess.TimeoutExpired as e:
            print(e)
            log.error(str(e))
            return ""
