#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import time
from conf import setting
import urllib
import urllib2
import json
import threading
from plugins import plugin_api
class ClientHander(object):
    def __init__(self):
        self.monitored_services = {}

    def load_latest_configs(self):
        '''
        load the latest monitor configs from monitor server
        :return:
        '''
        request_type = setting.configs['urls']['get_configs'][1]
        url = "%s/%s" %(setting.configs['urls']['get_configs'][0], setting.configs['HostID'])
        latest_configs = self.url_request(request_type,url)
        latest_configs = json.loads(latest_configs)
        self.monitored_services.update(latest_configs)



    def url_request(self,action,url,**extra_data):
        '''
        cope with monitor server by url
        :param action: "get" or "post"
        :param url: witch url you want to request from the monitor server
        :param extra_data: extra parameters needed to be submited
        :return:
        '''
        abs_url = "http://%s:%s/%s" % (setting.configs['Server'],
                                       setting.configs["ServerPort"],
                                       url)
        if action.lower() == 'get':
            print(abs_url,extra_data)
            try:
                req = urllib2.Request(abs_url)
                req_data = urllib2.urlopen(req,timeout=setting.configs['RequestTimeout'])
                callback = req_data.read()
                #print "-->server response:",callback
                return callback
            except urllib2.URLError,e:
                exit("\033[31;1m%s\033[0m"%e)

        elif action.lower() == 'post':
            #print(abs_url,extra_data['params'])
            try:
                data_encode = urllib.urlencode(extra_data['params'])
                req = urllib2.Request(url=abs_url,data=data_encode)
                res_data = urllib2.urlopen(req,timeout=setting.configs['RequestTimeout'])
                callback = res_data.read()
                callback = json.loads(callback)
                print "\033[31;1m[%s]:[%s]\033[0m response:\n%s" %(action,abs_url,callback)
                return callback
            except Exception,e:
                print('---exec',e)
                exit("\033[31;1m%s\033[0m"%e)

    def forever_run(self):
        '''
        start the client program forever
        :return:
        '''
        print "\033[32;1mBegin to start client\033[0m"
        exit_flag = False
        config_last_update_time = 0
        while not exit_flag:
            if time.time() - config_last_update_time > setting.configs['ConfigUpdateInterval']:
                self.load_latest_configs()
                print "\033[33;1mLoading latest config:\033[0m", self.monitored_services   #获取服务端的配置
                #{u'services': {u'LinuxCPU': [u'GetLinuxCpuStatus', 60], u'Nginx': [u'n/a', 60], u'Mysql': [u'n/a', 60],
                # u'LinuxNetwork': [u'GetLinuxNetworkStatus', 30], u'LinuxMemory': [u'GetLinuxMemStatus', 90]}}
                config_last_update_time = time.time()

            #根据服务端的配置，调取插件，获取监控的数据
            for service_name,val in self.monitored_services['services'].items():
                if len(val)==2:
                    self.monitored_services['services'][service_name].append(0)    #在服务端发送过来的配置信息中添加时间戳，开始为0
                monitor_interval = val[1]
                last_invoke_time = val[2]
                if time.time() - last_invoke_time >monitor_interval:
                    print( last_invoke_time,time.time())
                    self.monitored_services['services'][service_name][2] = time.time()

                    t = threading.Thread(target=self.invoke_plugin,args=(service_name,val))
                    t.start()

                else:
                    pass
                    # print "\033[32;1mprepare to monitor %s after %s sec \033[0m"%(
                    #     service_name,
                    #     monitor_interval - (time.time()-last_invoke_time)
                    # )


    def invoke_plugin(self,service_name,val):
        '''

        :param service_name:
        :param val:
        :return:
        '''
        plugin_name = val[0]
        if hasattr(plugin_api,plugin_name):
            func = getattr(plugin_api,plugin_name)
            plugin_callback = func()

            report_data = {
                'client_id':setting.configs['HostID'],
                'service_name':service_name,
                'data':json.dumps(plugin_callback)
            }

            request_action = setting.configs['urls']['service_report'][1]
            request_url = setting.configs['urls']['service_report'][0]

            print "\033[32;1m report data:\033[0m",report_data
            self.url_request(request_action,request_url,params=report_data)
        else:
            print "\033[31;1m have no plugin named %s in plugin_api.py \033[0m" %plugin_name
        print "--plugin:",val