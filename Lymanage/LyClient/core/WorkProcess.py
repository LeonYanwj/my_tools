#_*_condeing:utf-8_*_
__author__ = 'Leonyan'

from core import info_collection
from conf import settings
import json,sys,os,datetime
import requests
from core import api_token

class ArgvHandler(object):
    def __init__(self,argv_list):
        self.argvs = argv_list
        self.parse_argv()

    def parse_argv(self):
        if len(self.argvs) > 1:
            if hasattr(self,self.argvs[1]):
                func = getattr(self,self.argvs[1])
                func()
            else:
                self.help_msg()
        else:
            self.help_msg()

    def help_msg(self):
        msg = '''
        collect_data       收集硬件信息
        run_forever
        get_asset_id
        report_asset       收集硬件信息并汇报
        '''
        print(msg)

    def collect_data(self):
        """
        obj: 实例化Infocollection类
        asset_data: 收集硬件信息
        :return:返回硬件信息字典
        """""
        obj = info_collection.InfoCollection()
        asset_data = obj.collect()
