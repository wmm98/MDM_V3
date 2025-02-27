import shutil
import datetime
from Common import config, process_shell, log
import pytest

if __name__ == '__main__':
    conf = config.Config()
    shell = process_shell.Shell()
    debug_log = log.MyLog()
    xml_report_path = conf.xml_report_path
    html_report_path = conf.html_report_path
    pro_path = conf.environment_properties_path

    env_path = pro_path
    shutil.copy(env_path, xml_report_path)
    allure_list = '--allure-features=stability_normal_release_ota'
    args = ['-s', '-q', '--alluredir', xml_report_path, allure_list]
    debug_log.info('当前测试集：%s' % allure_list)
    curr_time = datetime.datetime.now()
    debug_log.info('用例运行开始时间: %s' % curr_time)
    pytest.main(args)
    cmd = 'allure generate %s -o %s --clean' % (xml_report_path, html_report_path)
    try:
        shell.invoke(cmd)
    except Exception:
        # debug_log.error('@@@执行失败， 请检查环境配置！！！')
        raise

    # 打开报告
    end_time = datetime.datetime.now()
    testpreiod = end_time - curr_time
    debug_log.info('用例运行结束时间: %s' % end_time)
    debug_log.info('总耗时为: %s' % testpreiod)
