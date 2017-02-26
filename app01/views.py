#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

from app01 import models
from serializer import ClientHandler
from backends import data_optimization
from backends import data_processing
from monitor import settings
from backends import redis_conn
from serializer import get_host_trigger
REDIS_OBJ = redis_conn.redis_conn(settings)
import serializer
import graphs

def client_configs(request,client_id):
    print "\033[31;1mthe client %s begin to get configuration\033[0m" %client_id
    config_obj = ClientHandler(client_id)
    config = config_obj.fetch_configs()

    if config:
        return HttpResponse(json.dumps(config))

@csrf_exempt
def service_data_report(request):
    if request.method =='POST':
        print "\033[32;1m--->\033[0m",request.POST
        #{'service_name': u'LinuxNetwork', 'data': '{"status": 0, "data": {"lo": {"t_in": "0.00", "t_out": "0.00"},
        # "virbr0": {"t_in": "0.00", "t_out": "0.00"},
        #  "virbr0-nic": {"t_in": "0.00", "t_out": "0.00"}, "eth0": {"t_in": "0.02", "t_out": "0.01"}}}', 'client_id': 2}
        try:
            print "host=%s,service=%s" %(request.POST.get('client_id'),request.POST.get('service_name'))
            data = json.loads(request.POST['data'])
            client_id = request.POST.get('client_id')
            service_name = request.POST.get('service_name')
            redis_obj = redis_conn.redis_conn(settings)
            data_saving_obj = data_optimization.DataStore(client_id,service_name,data,redis_obj)    #数据优化,并且存入redis DB中

            host_obj = models.Host.objects.get(id=client_id)
            service_trigger = get_host_trigger(host_obj)

            trigger_hander = data_processing.DataHander(settings,connect_redis=False)
            for trigger in service_trigger:
                trigger_hander.load_service_data_and_calulating(host_obj,trigger,redis_obj)

            print "\033[32;1m service trigger:",service_trigger
        except IndexError as e:
            print '\033[31;1m----err:\033[0m',e
    return HttpResponse(json.dumps('\033[34;1m---report data succ----\033[0m'))

def index(request):
    return render(request,'app01/index.html')

def dashboard(request):
    return render(request,'app01/dashboard.html')

def triggers(request):
    return render(request,'app01/triggers.html')

def hosts(request):
    host_list = models.Host.objects.all()
    print("hosts:",host_list)
    return render(request,'app01/hosts.html',{'host_list':host_list})

def host_detail(request,host_id):
    host_obj = models.Host.objects.get(id=host_id)
    return render(request,'app01/host_detail.html',{'host_obj':host_obj})


def host_detail_old(request,host_id):
    host_obj = models.Host.objects.get(id=host_id)

    config_obj = ClientHandler(host_obj.id)
    monitored_services = {
            "services":{},
            "sub_services": {} #存储一个服务有好几个独立子服务 的监控,比如网卡服务 有好几个网卡
        }

    template_list= list(host_obj.templates.select_related())

    for host_group in host_obj.host_groups.select_related():
        template_list.extend( host_group.templates.select_related() )
    print(template_list)
    for template in template_list:
        #print(template.services.select_related())

        for service in template.services.select_related(): #loop each service
            print(service)
            if not service.has_sub_service:
                monitored_services['services'][service.name] = [service.plugin_name,service.interval]
            else:
                monitored_services['sub_services'][service.name] = []

                #get last point from redis in order to acquire the sub-service-key
                last_data_point_key = "StatusData_%s_%s_latest" %(host_obj.id,service.name)
                last_point_from_redis = REDIS_OBJ.lrange(last_data_point_key,-1,-1)[0]
                if last_point_from_redis:
                    data,data_save_time = json.loads(last_point_from_redis)
                    if data:
                        service_data_dic = data.get('data')
                        for serivce_key,val in service_data_dic.items():
                            monitored_services['sub_services'][service.name].append(serivce_key)
    return render(request,'host_detail.html', {'host_obj':host_obj,'monitored_services':monitored_services})

def trigger_list(request):

    trigger_handle_obj = serializer.TriggersView(request,REDIS_OBJ)
    trigger_data = trigger_handle_obj.fetch_related_filters()

    return render(request,'app01/trigger_list.html',{'trigger_list':trigger_data})

def hosts_status(request):
    hosts_data_serializer = serializer.StatusSerializer(request,REDIS_OBJ)
    hosts_data = hosts_data_serializer.by_hosts()

def graphs_gerator(request):

    graphs_generator = graphs.GraphGenerator2(request,REDIS_OBJ)
    graphs_data = graphs_generator.get_host_graph()

    return HttpResponse(json.dumps(graphs_data))