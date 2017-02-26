#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'Charles Chang'

configs = {
    'HostID':2,
    'Server':"192.168.1.103",
    "ServerPort":8080,
    "urls":{
        'get_configs':['api/client/config','get'],
        'service_report':['api/client/service/report/','post'],
    },
    'RequestTimeout':30,
    'ConfigUpdateInterval':300,  #默认5分钟
}
