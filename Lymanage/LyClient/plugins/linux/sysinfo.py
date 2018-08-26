#_*_conding:utf-8_*_
__author__ = 'Leonyan'

import platform
import json
import subprocess
import re

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
        data = []
        result = subprocess.Popen("dmidecode -t 17",shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE).stdout.read().decode("utf-8")
        info = re.findall(r"Memory Device\n\t(.*)\n\t(.*)\n\t(.*)\n\t(.*)\n\t(.*)\n\t(.*)\n\t(.*)\n\t(.*)\n\t(.*)\n\t(.*)\n\t(.*)\n\t(.*)\n\t(.*)\n\t(.*)\n\t(.*)\n\t(.*)\n\t(.*)\n\t(.*MHz)",result)
        try:
            for line in info:
                ram_data = {}
                ram_data['capacity'] = line[4].split(": ")[1]
                ram_data['slot'] = line[7].split(": ")[1]
                ram_data['model'] = line[9].split(": ")[1]
                ram_data['manufactory'] = line[12].split(": ")[1]
                ram_data['sn'] = line[13].split(": ")[1]
                data.append(ram_data)
        except Exception as e:
            print(e)

        return {"ram": data}


def nicinfo():
    #tmp_f = file('/tmp/bonding_nic').read()
    #raw_data= subprocess.check_output("ifconfig -a",shell=True)
    # raw_data = subprocess.Popen("ifconfig -a",shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE).stdout.read().decode("utf-8")
    raw = open(r'C:\Users\Administrator\my_tools\Lymanage\LyClient\1.txt','r',encoding='utf-8')
    raw_data = raw.read()

    raw_data= raw_data.split("\n")

    nic_dic = {}
    next_ip_line = False
    last_mac_addr = None
    for line in raw_data:
        if next_ip_line:
            #print last_mac_addr
            #print line #, last_mac_addr.strip()
            next_ip_line = False
            nic_name = last_mac_addr.split()[0]
            mac_addr = last_mac_addr.split("HWaddr")[1].strip()
            raw_ip_addr = line.split("inet addr:")
            raw_bcast = line.split("Bcast:")
            raw_netmask = line.split("Mask:")
            if len(raw_ip_addr) > 1: #has addr
                ip_addr = raw_ip_addr[1].split()[0]
                network = raw_bcast[1].split()[0]
                netmask =raw_netmask[1].split()[0]
                #print(ip_addr,network,netmask)
            else:
                ip_addr = None
                network = None
                netmask = None
            if mac_addr not in nic_dic:
                nic_dic[mac_addr] = {'name': nic_name,
                                     'macaddress': mac_addr,
                                     'netmask': netmask,
                                     'network': network,
                                     'bonding': 0,
                                     'model': 'unknown',
                                     'ipaddress': ip_addr,
                                     }
            else: #mac already exist , must be boding address
                if '%s_bonding_addr' %(mac_addr) not in nic_dic:
                    random_mac_addr = '%s_bonding_addr' %(mac_addr)
                else:
                    random_mac_addr = '%s_bonding_addr2' %(mac_addr)

                nic_dic[random_mac_addr] = {'name': nic_name,
                                     'macaddress':random_mac_addr,
                                     'netmask': netmask,
                                     'network': network,
                                     'bonding': 1,
                                     'model': 'unknown',
                                     'ipaddress': ip_addr,
                                     }

        if "HWaddr" in line:
            #print line
            next_ip_line = True
            last_mac_addr = line

    raw.close()
    nic_list= []
    for k,v in nic_dic.items():
        nic_list.append(v)

    return {'nic':nic_list}


print(nicinfo())