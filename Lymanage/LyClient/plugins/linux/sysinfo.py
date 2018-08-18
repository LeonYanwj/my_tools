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
        data = []
        cpu_info = {
            'cpu_model': "dmidecode -t processor|grep 'Version'|sed -n 1p|awk -F: '{print $NF}'",
            'cpu_count': "dmidecode -t processor|grep 'Processor Information'|wc -l'",
            'cpu_core_count': "dmidecode -t processor|grep ''Core Enabled'|awk -F: '{sum+=$2};END{print sum}'",
            'cpu_thread_count' : "dmidecode -t processor|grep 'Thread Count'|awk -F: '{sum+=$2};END{print sum}'",
        }

        for k,cmd in cpu_info.items():
            try:
                res = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE).stdout.read().strip()
                cpu_info[k] = res
            except ValueError as e:
                #此处需要记录日志
                print(e)

        count = int(cpu_info.get('cou_count'))
        for i in range(count):
            data.append(cpu_info)

        return {"cpu_info":data}

    def get_ram(self):
        pass




