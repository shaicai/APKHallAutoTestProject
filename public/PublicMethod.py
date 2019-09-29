# coding=utf-8
"""
This is Public Method.
"""
import re
import yaml
from airtest.core.api import *
from poco.drivers.std import StdPoco


class PublicMethod:
    """
    This is Public Method.
    """

    def getFiles(dir, suffix):  # 查找根目录，文件后缀
        res = []
        for root, directory, files in os.walk(dir):  # =>当前根,根下目录,目录下的文件
            for filename in files:
                name, suf = os.path.splitext(filename)  # =>文件名,文件后缀
                if suf == suffix:
                    res.append(os.path.join(root, filename))  # =>吧一串字符串组合成路径
        return res

    def InstallAPK(self):

        '''
        获取电脑连接的手机列表，获取连接手机的设备号dev1
        :return:
        '''
        list = []
        out = os.popen("adb devices")
        for i in out.readlines():
            if 'List of devices' in i or "adb" in i or 'daemon' in i:
                pass
            elif "unauthorized" in i or len(i) < 5:
                pass
            elif 'offline' in i or "unauthorized" in i:
                pass
            else:
                serial = re.findall('(.*?)\\tdevice', i)
                s = ','.join(serial)
                list.append(s)
        dev1 = connect_device("Android://127.0.0.1:5037/" + list[0])

        # 获取手机安装的包的情况，判断手机是否装有包，未装包，则安装指定包
        apk_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        data = PublicMethod().operateYaml(apk_path + "/data/Login.yaml")  # 读取yaml数据表的值
        global package
        package = data['Setting']['apk_package']['packagename']
        list = os.popen("adb shell pm list package "+package).readlines()
        file = PublicMethod.getFiles("F:\\APKHallAutoTestProject\\public\\app", '.apk')
        # 查找以.apk结尾的文件
        if not file:
            print("环境中没有可用的apk文件，请检查")
            quit()
        if len(file) >= 2:
            print("环境中存在多个可用的apk文件，请检查")
            quit()
        i = 0
        # 判断list是否为空
        if not list:
            i = 1
        else:
            for line in list:
                if line == "package:"+package+"\n":
                    i = 0
                    break
                else:
                    i = 1
        if i == 1:
            dev1.install_app(file[0])

    def HandleAuthority(self):
        '''
        处理初次启动App时的权限允许弹框
        :return:
        '''
        #  处理隐私信息获取弹框
        sleep(6)
        for i in range(1, 4):
            if exists(Template(r"tpl1569294479081.png", record_pos=(0.193, 0.35), resolution=(720, 1280))):
                touch(Template(r"tpl1569294479081.png", record_pos=(0.193, 0.35), resolution=(720, 1280)))
                break
            else:
                sleep(1)
        from poco.drivers.android.uiautomation import AndroidUiautomationPoco
        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
        for i in range(1, 7):
            try:
                tips_xiaomi = poco(text=("允许"))
                if tips_xiaomi:
                    tips_xiaomi.click()
            except:
                pass
            try:
                tips_huawei = poco(text=("始终允许"))
                if tips_huawei:
                    tips_huawei.click()
            except:
                pass
            sleep(2)

    def HandleInterfacaBox(self):
        '''
        处理初次进入界面可能弹出的活动弹窗
        :return:
        '''
        from poco.drivers.android.uiautomation import AndroidUiautomationPoco
        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
        try:
            tips_realname = poco(package+":id/bt_dialog_close")  # 弹框的关闭按钮
            if tips_realname:
                tips_realname.click()
        except:
            pass
        sleep(2)
        poco = StdPoco()
        try:
            tips_change_name = poco("JJButtondialog_close_btn_n")
            # 弹框的关闭按钮
            biaoshi = poco("SceneBaseRootView").child("JJViewGroup")[0].\
                child("JJImagepage_indicator_common")[1]
            # 大厅下方的页标识
            if tips_change_name:
                biaoshi.click()
        except:
            pass
        sleep(2)

    def operateYaml(self, filename):
        '''
        读取Yaml文件
        :param filename: 读取Yaml文件的名称
        :return:
        '''
        file = open(filename, "r", encoding='utf-8')
        data = yaml.load(file, Loader=yaml.FullLoader)
        file.close()
        return data

    def check_error(self):
        '''
        检查手机的DCIM文件夹中是否有lua__error开头的图片文件，（大厅机制为出现error会自动截图到此文件夹）
        :return:
        '''
        w = os.popen("adb shell ls /sdcard/DCIM").readlines()
        i = 0
        for line in w:
            if 'lua_error' in line:
                i = 1
        return i

    def analysis_log(self):
        '''
        检查自动化测试期间手机中生成的log中是否存在error、warning及死机日志
        :return:
        '''
        day = time.strftime('%m%d', time.localtime(time.time()))
        error = 0
        warning = 0
        died = 0
        try:
            os.popen("adb pull sdcard/jjlog_lua_"+day+".log")
            sleep(10)
            thing = "jjlog_lua_"+day+".log"
            for i in range(1, 10):
                if os.path.exists(thing):
                    filename = thing  # txt文件和当前脚本在同一目录下，所以不用写具体路径
                    #  errors="ignore" 忽略log中的编码问题
                    with open(filename, 'r', encoding='UTF-8', errors="ignore") as file_to_read:
                            for row in file_to_read:
                                #  检查log中是否存在error
                                if 'LUA ERROR' in row:
                                    error = 1
                                #  检查log中是否存在warning
                                if 'Lua Warning' in row:
                                    warning = 1
                                #  检查log是否存在死机，卡死
                                if 'died' in row:
                                    died = 1
                    break
                else:
                    sleep(5)
        except:
            pass
        return error, warning, died
