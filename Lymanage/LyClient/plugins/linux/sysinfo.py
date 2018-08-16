#_*_conding:utf-8_*_
__author__ = 'Leonyan'

import platform
import json
import subprocess

def collect():
    data = {
        'os_type': platform.system(),
        'asset_type': 'server',
    }

class LinuxAssetInfo(object):
    def __init__(self):
        pass

    def get_cpuinfo(self):
        data = {}