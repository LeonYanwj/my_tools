#!/bin/bash

hostname=`hostname`
disk=`df -Th|sed -n 2p|awk '{print $6}'`

total=`free -m |sed -n 2p|awk '{print $2}'`
use=`free -m |sed -n 2p|awk '{print $3}'`
buffer=`free -m |sed -n 2p|awk '{print $6}'`
cache=`free -m |sed -n 2p|awk '{print $7}'`
real_use=`expr $use - $buffer - $cache`

real_use_rate=`echo |awk '{print '$real_use'/'$total'*100"%"}'`

cpu_rate=`vmstat |awk '{print $15}'|tail -n1`

io=`uptime |awk '{print $NF}'`

echo -e "\033[35mhostname:$hostname\033[0m"
echo -e "\033[32mCPU空闲：$cpu_rate\t内存使用：$real_use_rate\t磁盘剩余：$disk\t负载：$io\033[0m"
