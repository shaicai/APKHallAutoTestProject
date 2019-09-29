# coding:utf-8
import HTMLTestRunner
import unittest
from case import casedemo
import os
#获取路径
ABSPATH = os.path.abspath(os.path.realpath(os.path.dirname(__file__)))


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(casedemo.MyTestCase("test_one"))
    suite.addTest(casedemo.MyTestCase("test_something"))

    #如果没指定路径需要创建路径
    path=ABSPATH
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        pass
    report_path = "report.html"
    report_title = u"测试报告"
    desc = u"接口自动化测试报告详情"


    fp = open(report_path, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(fp, title=report_title, description=desc)
    runner.run(suite)
