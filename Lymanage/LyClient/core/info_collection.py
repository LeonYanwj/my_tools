#_*_conding:utf-8_*_
__author__ = 'Leonyan'

from plugins import plugin_api
import json,platform,sys

class InfoCollection(object):
    def __init__(self):
        pass

    def get_platform(self):
        #获取执行脚本的系统型号
        os_platform = platform.system()
        return os_platform

    def collect(self):
        """
        os_platform:是获取当前系统类型，返回的是Windows或者是Linux
        func： 反射获取Windows或者是Linux方法
        :return:
        """
        os_platform = self.get_platform()
        try:
            func = getattr(self,os_platform)
            info_data = func()
            formatted_data = self.build_report_data(info_data)
            return formatted_data

        except AttributeError as error:
            sys.exit("Error:MadKing doens't support os [%s]! " % os_platform)

    def Linux(self):
        sys_info = plugin_api.LinuxSysInfo()
        return sys_info

    def Windows(self):
        sys_info = plugin_api.WindowsSysInfo()
        return sys_info

    def build_report_data(self,data):
        return data