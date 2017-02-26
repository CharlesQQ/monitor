#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'Charles Chang'

from linux import sysinfo,load,cpu_mac,cpu,memory,network,host_alive,nginx,mysql

def LinuxSysInfo():
    #print __file__
    return  sysinfo.collect()

def GetLinuxCpuStatus():
    return cpu.monitor()

def host_alive_check():
    return host_alive.monitor()
def GetMacCPU():
    #return cpu.monitor()
    return cpu_mac.monitor()
def GetLinuxNetworkStatus():
    return network.monitor()

def GetLinuxMemStatus():
    return memory.monitor()

def GetNginxStatus():
    return nginx.monitor()

def GetMysqlStatus():
    return mysql.monitor()