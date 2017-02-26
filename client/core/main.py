#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'Charles Chang'
import client_sender

class command_hander(object):

    def __init__(self,sys_args):
        self.sys_args = sys_args
        if len(self.sys_args) <2:    #判断命令输入的参数的个数
            exit(self.help_msg())
        self.command_allowcator()

    def command_allowcator(self):
        print self.sys_args[1]
        if hasattr(self,self.sys_args[1]):
            func = getattr(self,self.sys_args[1])
            return func()
        else:
            print("\033[31m命令行参数不存在\033[0m")
            self.help_msg()

    def help_msg(self):
        valid_commands = """\033[32m
        start   启动监控的client
        stop    停止监控的client\033[0m"""
        exit(valid_commands)

    def start(self):
        print "\033[32m开始启动监控的客户端\033[0m"
        Client = client_sender.ClientHander()
        Client.forever_run()

    def stop(self):
        print "\033[32m开始停止监控的客户端\033[0m"
