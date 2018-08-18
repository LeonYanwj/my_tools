#_*_conding:utf-8_*_
__author__ = 'Leonyan'

from plugins.linux import sysinfo


def LinuxSysInfo():
    return sysinfo.collect()

def WindowsSysInfo():
    from plugins.windows import sysinfo as win_sysinfo
    return win_sysinfo.collect()