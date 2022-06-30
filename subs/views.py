from django.shortcuts import render
from .forms import addIP_text, addIP_file
from django.http import HttpResponse, QueryDict
from json import dumps
from Packages.running_out_of_toner import *
from Packages.SubPkg.foos import *
from Packages.PlotData import *
from Packages.FormObjClass import *
from Packages.StrucData import *
from Packages.ViewRequestHandle import *


def PrintMonitor(request):
    if request.GET.get('user'):
        user = request.GET.get('user')
        request_handle = ViewRequestHandler(user, 'PrinterMonitor')
        request_handle.get_request(request)
        form = CreateForm('PrinterMonitor')
        formObj = form.PrinterMonitor(request_handle.page_modifier)
        data2json = dumps(get_table_data(request_handle.page_modifier['filter']))
        return render(request, 'monitor.html', {'data': data2json, 'user': user, 'form': formObj}) #'filter': filter})  #data2json})


def details(request):
    if request.GET.get('user'):
        user = request.GET['user']
        id = request.GET.get('id', '')
        head, data = get_device_detail(id)
        head['ID'] = id
        request_handle = ViewRequestHandler(user, 'DeviceDetails', data_mod=ddf(head))
        request_handle.get_request(request)
        head, data = get_device_detail(id)
        data2json = dumps(data)
        send = {'user': user, 'data': data2json, 'id': id, 'debug': request_handle.debug}
        send.update(ddf(head))
        return render(request, 'device_detail.html', send)


def cartTrack(request):
    if request.GET.get('user'):
        user = request.GET['user']
        request_handle = ViewRequestHandler(user, 'CartStorage')
        request_handle.get_request(request)
        form = CreateForm('CartridgeStorage')
        formObj = form.CartStorage(request_handle.page_modifier)
        tracker = CartStoreTracker()
        index, arr = tracker.process_time(int(request_handle.CartStoreDays()), filter_mode=request_handle.page_modifier['filter_mode'])
        data2json = dumps(tracker.table_data)
        return render(request, 'cartTracker.html', {'index': index, 'sets': arr,
                                                    'data': data2json, 'user': user,
                                                    'form': formObj, 'debug': request_handle.debug})


def analytics(request):
    if request.GET.get('user'):
        user = request.GET['user']
        t_dic = read_conf(user, 'analytics')
        if len(t_dic.keys()) == 0:
            t_dic = {'group': 'Manufacture', 'value': 'BW', 'filter': ''}
        if request.GET.get('group'):
            t_dic['group'] = request.GET['group']
        if request.GET.get('value'):
            t_dic['value'] = request.GET['value']
        if request.GET.get('filter'):
            t_dic['filter'] = request.GET['filter']
        write_conf(user, 'analytics', t_dic)
        if t_dic['value'] in ['BW', 'BCYM']:
            data_arr = create_plot_data(t_dic['group'], t_dic['filter'], t_dic['value'])
            index = get_global_timeline()
            conf = {'type': 'line', 'data': {'labels': index, 'datasets': data_arr}, 'options': {}}
        elif 'Total' in t_dic['value']:
            conf = create_pie_chart(t_dic['group'], t_dic['filter'], t_dic['value'])
        else:
            conf = create_bar_data(t_dic['group'], t_dic['filter'], t_dic['value'])
        form = CreateForm('Analytics')
        formObj = form.Analytics(t_dic)
        return render(request, 'analytics.html', {'user': user, 'conf': conf, 'form': formObj})


def config(request):
    if request.GET.get('user'):
        user = request.GET.get('user')
        if request.GET.get('details'):
            details = request.GET.get('details')
            write_conf(user, ('details', details))
        return render(request, 'config.html', {'user': user})


def dmgr(request):
    if request.GET.get('user'):
        user = request.GET['user']
        request_handle = ViewRequestHandler(user, 'DeviceManager')
        request_handle.get_request(request)
        data2json = dumps(get_pending_ip())
        form = CreateForm('DeviceManager')
        formObj = form.DeviceManager()
        return render(request, 'devMgr.html', {'user': user, 'data': data2json, 'form':formObj})

