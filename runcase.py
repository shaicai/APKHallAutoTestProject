import os
import unittest
import sys
import logging
import re
from airtest.core.api import *
import time
from public.sendemails import SendEmails
from report import HTMLTestRunner
from public.PublicMethod import PublicMethod
proDir = os.path.split(os.path.realpath(__file__))[0]
airtest_logger = logging.getLogger("airtest")
airtest_logger.setLevel(logging.INFO)


# 设置执行的case
def read_case_list():
    case_list_file = os.path.join(proDir, "caselist.txt")
    fb = open(case_list_file)
    case_list = []
    for value in fb.readlines():
        data = str(value)
        if data != '' and not data.startswith("#"):
            case_list.append(data.replace("\n", ""))
    fb.close()
    return case_list


# 设置测试套件
def set_case_suite():
    case_list = read_case_list()
    suite_module = []
    case_file = os.path.join(proDir, "testcase")
    test_suite1 = unittest.TestSuite()
    for case in case_list:
        case_name = case.split("/")[-1]
        discover = unittest.defaultTestLoader.discover(case_file, pattern=case_name + '.py', top_level_dir=None)
        suite_module.append(discover)
    if len(suite_module) > 0:
        for suite in suite_module:
            for test_name in suite:
                test_suite1.addTest(test_name)
    else:
        pass
    return test_suite1


def report_path():
    path = "F:\\APKHallAutoTestProject\\"
    sys.path.append(path)
    dir1 = os.path.abspath(os.curdir)
    result = dir1 + "\\report\\"
    # 获取系统当前时间
    now = time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(time.time()))
    day = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    # 定义个报告存放路径，支持相对路径
    tdresult = result + day

    # 检验文件夹路径是否已经存在
    if not os.path.exists(tdresult):
        tdresult.rstrip("\\")
        os.makedirs(tdresult)  # 创建测试报告文件夹
    filename1 = tdresult + "/" + now + "_result.html"
    return filename1


def uninstallapk():
    '''
    卸载手机之前安装的app，保证使用的是最新的测试代码
    :return:
    '''
    apk_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
    data = PublicMethod().operateYaml(apk_path + "/data/Login.yaml")  # 读取yaml数据表的值
    list1 = os.popen("adb shell pm list package "+data['Setting']['apk_package']['packagename']).readlines()
    for line in list1:
        if line == "package:"+data['Setting']['apk_package']['packagename']+"\n":
            os.system("adb uninstall "+data['Setting']['apk_package']['packagename'])
    #  删除手机DCIM文件夹下的图片文件
    # w = os.popen("adb shell ls /sdcard/DCIM").readlines()
    # if len(w) != 0:
    #     os.popen("adb shell rm /sdcard/DCIM/*.jpg")
    #  删除手机根目录下的当天的lua的log文件
    day = time.strftime('%m%d', time.localtime(time.time()))
    os.popen("adb shell rm -f /sdcard/jjlog_lua_" + day + ".log")


def get_devices_information():
    '''
    获取电脑连接的手机列表，获取连接手机的设备号dev1
    :return:
    '''
    list=[]
    out = os.popen("adb devices")
    for i in out.readlines():
        if 'List of devices' in i or "adb" in i or 'daemon' in i or 'offline' in i or "unauthorized" in i or len(
                i) < 5:
            pass
        else:
            serial = re.findall('(.*?)\\tdevice', i)
            s1 = ','.join(serial)
            list.append(s1)
    dev1 = connect_device("Android://127.0.0.1:5037/" + list[0])
    return dev1


# 报告执行
dev1 = get_devices_information()
dev1.start_recording()
uninstallapk()
test_suite = set_case_suite()
filename = report_path()
if test_suite is not None:
    # 定义测试报告
    fp = open(filename, 'wb')
    # 执行测试报告
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u"APK大厅自动化测试报告", description=u"UI自动化测试报告详情")
    # 运行测试用例
    runner.run(test_suite)
    fp.close()
else:
    pass
sendemail = SendEmails()
sendemail.sendemails(filename)
dev1.stop_recording()



