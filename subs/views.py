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
        #if request.GET.get('filter'):
        #    filter = request.GET.get('filter')
        #    t_dic = {'filter': filter}
        #    write_conf(user, 'printer_monitor', t_dic)
        #else:
        #    t_dic = read_conf(user, 'printer_monitor')
        #    filter = t_dic['filter']
        form = CreateForm('PrinterMonitor')
        #formObj = form.PrinterMonitor(t_dic)
        formObj = form.PrinterMonitor(request_handle.page_modifier)
        #data2json = dumps(get_table_data(t_dic['filter']))
        data2json = dumps(get_table_data(request_handle.page_modifier['filter']))

        #return render(request, 'monitor.html', {'data': data2json, 'user': user, 'form': formObj}) #'filter': filter})  #data2json})
        return render(request, 'monitor.html', {'data': data2json, 'user': user, 'form': formObj}) #'filter': filter})  #data2json})


def details(request):
    if request.GET.get('user'):
        user = request.GET['user']
        id = request.GET.get('id', '')
        head, data = get_device_detail(id)
        request_handle = ViewRequestHandler(user, 'DeviceDetails', data_mod=head)
        request_handle.get_request(request)
        head, data = get_device_detail(id)
        data2json = dumps(data)
        formOR = device_detail_form_obj(head, request_handle.page_modifier['access'])
        return render(request, 'device_detail.html', {'user': user,
                                                      'data': data2json,
                                                      'form': formOR, 'id': id,
                                                      'debug': request_handle.debug})
'''override_entry = False
        try:
            if request.GET.get('override-this'):
                key = request.GET.get('override-this')
                if request.GET.get('with'):
                    val = request.GET.get('with')
                    override_entry = {key: val}
                else:
                    override_entry = {key: ''}
        except:
            override_entry = False
        id = request.GET.get('id', '')
        if override_entry is not False:
            override = LibOverride()
            override.addEntry(id, override_entry)
        t_dic = read_conf(user, 'printer_details')
        time = t_dic['time']
        vals = t_dic['vals']
        if request.GET.get('time'):
            time = request.GET.get('time')
            t_dic['time'] = time
        if request.GET.get('vals'):
            vals = request.GET.get('vals')
            t_dic['vals'] = vals
        write_conf(user, 'printer_details', t_dic)
        data, head = get_details_data(id, time, vals)
        data2json = dumps(data)
        page = 'details.html' if vals == 'grouped' else 'details2.html'
        return render(request, page, {'user': user, 'times': time,
                                                'data': data2json,
                                                'h1': head(),
                                                'h2': head(line='2'),
                                                'id': id})
        '''

def cartTrack(request):
    if request.GET.get('user'):
        user = request.GET['user']
        request_handle = ViewRequestHandler(user, 'CartStorage')
        request_handle.get_request(request)
        form = CreateForm('CartridgeStorage')
        formObj = form.CartStorage(request_handle.page_modifier)
        tracker = CartStoreTracker()
        index, arr = tracker.process_time(int(request_handle.page_modifier['days']))
        data2json = dumps(tracker.table_data)
        return render(request, 'cartTracker.html', {'index': index, 'sets': arr,
                                                    'data': data2json, 'user': user,
                                                    'form': formObj}) # 'days': days, })

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
        else:
            conf = create_bar_data(t_dic['group'], t_dic['filter'], t_dic['value'])
        form = CreateForm('Analytics')
        formObj = form.Analytics(t_dic)
        return render(request, 'analytics.html', {'user': user, #'index': index, 'sets': data_arr,
                                                   'conf': conf, 'form': formObj})
                                                  #'group': t_dic['group'], 'filter': t_dic['filter'], 'value': t_dic['value']})

def config(request):
    if request.GET.get('user'):
        user = request.GET.get('user')
        if request.GET.get('details'):
            details = request.GET.get('details')
            write_conf(user, ('details', details))
        return render(request, 'config.html', {'user': user})

def dmgr(request):
    ip = request.GET.get('add_ip', '')
    if ip != '':
        handle_ip_form(ip)
    try:
        if request.GET.get('remove'):
            remove = request.GET.get('remove')
            arr = get_pending_ip()
            t_arr = []
            for i in arr:
                if remove != i['IP']:
                    t_arr.append(i)
            update_ip_form(t_arr)
    except:
        remove = ''
    data2json = dumps(get_pending_ip())
    return render(request, 'devMgr.html', {'data': data2json})
