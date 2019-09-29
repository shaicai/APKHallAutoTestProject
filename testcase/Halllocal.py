# -*-encoding:utf-8 -*-
import unittest
from airtest.core.api import *
from poco.drivers.std import StdPoco
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from public.PublicMethod import PublicMethod

apk_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
data = PublicMethod().operateYaml(apk_path + "/data/login.yaml")  # 读取yaml数据表的值
package = data['Setting']['apk_package']['packagename']


def login(accountpye):
    '''
    通用的切换账号的方法
    :param accountpye: 测试账号的编号
    :return:
    '''
    poco = StdPoco()
    text(data['login'][accountpye]['username'])  # 输入用户名


class Halllocal(unittest.TestCase):
    u'''大厅基础界面相关'''

    def setUp(self):
        auto_setup(__file__)  # 初始化Airtest所需的一些连接
        poco = StdPoco()
        PublicMethod().InstallAPK()  # 未安装测试apk时，安装测试apk
        start_app(package)  # 启动APK
        PublicMethod().HandleAuthority()  # 处理启动APP时的权限弹框
        sleep(7.0)

    # @unittest.skip("CaseTest")
    def testcase01(self):
        u'''示例case1'''
        poco = StdPoco()
        sleep(2.0)
        PublicMethod().HandleInterfacaBox()  # 处理进入APK大厅后可能出现的活动窗口
        sleep(2.0)
        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
        sleep(2.0)
        poco("android:id/tabs").child(package+":id/footer_bg")[3].child(package+":id/animation_view").click()  # 点击我页签
        sleep(2.0)

    def testcase02(self):
        u'''示例case2'''
        login('changeaccount')
        poco = StdPoco()
        sleep(3.0)
        poco = StdPoco()
        touch(Template(r"tpl1559804215578.png", record_pos=(-0.227, 0.07), resolution=(1280, 720)))  #
        sleep(60.0)

    def tearDown(self):
        pass
        clear_app(package)
