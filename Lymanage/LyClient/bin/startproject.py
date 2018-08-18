#_*_conding:utf-8_*_
__author__ = 'Leonyan'

import os,sys,platform

if platform.system() == "Windows":
    #将脚本执行路径添加到Python的系统变量中
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    print(BASE_DIR)
else:
    BASE_DIR = '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])

sys.path.append(BASE_DIR)

from core import WorkProcess

if __name__ == '__main__':
    #run script with parameter,first is script name second is location parameter
    WorkProcess.ArgvHandler(sys.argv)