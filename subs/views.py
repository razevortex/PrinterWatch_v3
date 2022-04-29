from django.shortcuts import render
from .forms import addIP_text, addIP_file
from django.http import HttpResponse, QueryDict
from json import dumps
from Packages.running_out_of_toner import *
from Packages.SubPkg.foos import *
from Packages.PlotData import *
from Packages.StrucData import *


def PrintMonitor(request):
    if request.GET.get('user'):
        user = request.GET.get('user')
        if request.GET.get('filter'):
            filter = request.GET.get('filter')
            t_dic = {'filter': filter}
            write_conf(user, 'printer_monitor', t_dic)
        else:
            t_dic = read_conf(user, 'printer_monitor')
            filter = t_dic['filter']

        data2json = dumps(get_table_data(filter))
        return render(request, 'monitor.html', {'data': data2json, 'user': user, 'filter': filter})  #data2json})

'''
def PrintMonitor(request):
    filter = request.GET.get('filter', '')

    if request.GET.get('user'):
        user = request.GET.get('user')
        if filter == '':
            t_dic = read_conf(user, 'printer_monitor')
            filter
        data2json = dumps(get_table_data(filter))
        return render(request, 'monitor.html', {'data': data2json, 'user': user, 'filter': filter})  # data2json})
'''

def details(request):
    if request.GET.get('user'):
        user = request.GET['user']
        override_entry = False
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
def details(request):
    override_entry = False
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
    fuse = [('TonerC', 'TonerM', 'TonerY'),
            ('Printed_BW', 'Copied_BW'),
            ('Printed_BCYM', 'Copied_BCYM')]
    to = ['TonerCYM', 'PagesBW', 'PagesBCYM']
    id = request.GET.get('id', '')
    if override_entry is not False:
        override = LibOverride()
        override.addEntry(id, override_entry)

    conf = 'total'
    if request.GET.get('user'):
        user = request.GET['user']
        conf = read_conf(user)
        conf = conf['details']
    data, head = get_details_data(id, conf)
    container = DataSet(id)
    container.light_Data()
    container.diff_Data()
    for i in range(len(fuse)):
        container.combine_keys(fuse[i], to[i])
    container.sum_data()
    data2json = dumps(data)#container.table_data())
    return render(request, 'details.html', {'data': data2json,
                                            'h1': container.head_data(),
                                            'h2': container.head_data(line='2'),
                                            'id': id})

'''
def cartTrack(request):
    if request.GET.get('user'):
        user = request.GET['user']
        t_dic = read_conf(user, 'cart_monitor')
        try:
            days = t_dic['days']
        except:
            days = 10

        ctyp = ''
        cadd = ''

        if request.GET.get('days'):
            days = request.GET['days']
        t_dic['days'] = days

        try:
            if request.GET.get('cart'):
                ctyp = request.GET['cart']
        except:
            ctyp = ''
        try:
            if request.GET.get('num'):
                cadd = request.GET['num']
        except:
            cadd = ''

        if ctyp != '' and cadd != '':
            temp = add_to_Storage(ctyp, cadd, Storage2Dict())
            UpdateStorage(temp)

        else:
            days = int(days)
        write_conf(user, 'cart_monitor', t_dic)

        tracker = CartStoreTracker()
        index, arr = tracker.process_time(int(days))
        data2json = dumps(tracker.table_data)
        return render(request, 'cartTracker.html', {'index': index, 'sets': arr, 'data': data2json, 'days': days, 'user': user,})


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
        data_arr = create_plot_data(t_dic['group'], t_dic['filter'], t_dic['value'])
        index = get_global_timeline()

        return render(request, 'analytics.html', {'user': user, 'index': index, 'sets': data_arr, 'group': t_dic['group'], 'filter': t_dic['filter'], 'value': t_dic['value']})

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
