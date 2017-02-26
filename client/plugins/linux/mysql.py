#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'Charles Chang'


import subprocess
def monitor():
    shell_command = 'ps -ef|grep -v grep |grep nginx|wc -l'
    result = subprocess.Popen(shell_command,shell=True,stdout=subprocess.PIPE).stdout.readlines()
    #print(result)
    value_dic = {'status':0,}
    for line in result:
        line = line.split()
        value_dic['mysql_process_num']=line[0]
        value_dic['test']=1
    return value_dic