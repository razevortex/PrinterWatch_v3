from django.shortcuts import render
from .forms import addIP_text, addIP_file
from django.http import HttpResponse, QueryDict
from json import dumps
from Packages.running_out_of_toner import *
from Packages.SubPkg.foos import *
from Packages.PlotData import *
from Packages.StrucData import *


def PrintMonitor(request):
    filter = request.GET.get('filter', '')
    data2json = dumps(filteredTableContent(filter))
    return render(request, 'monitor.html', {'data': data2json})


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
    container = DataSet(id)
    container.light_Data()
    container.diff_Data()
    for i in range(len(fuse)):
        container.combine_keys(fuse[i], to[i])
    container.sum_data()
    data2json = dumps(container.table_data())
    return render(request, 'details.html', {'data': data2json,
                                            'h1': container.head_data(),
                                            'h2': container.head_data(line='2'),
                                            'id': id})


def cartTrack(request):
    days = 10
    ctyp = ''
    cadd = ''
    try:
        if request.GET.get('days'):
            days = request.GET['days']
    except:
        days = ''
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
    if days == '':
        days = 10
    else:
        days = int(days)
    data2json = dumps(cart_state(int(days)))
    return render(request, 'cartTracker.html', {'data': data2json, 'days': days})


def analytics(request):
    group = request.GET.get('group', 'Manufacture')
    value = request.GET.get('value', 'BW')
    filter = request.GET.get('filter', '')
    data_arr = create_plot_data(group, filter, value)
    index = get_global_timeline()
    string = f'{group}   /> {value}   /> {filter}'
    return render(request, 'analytics.html', {'index': index, 'sets': data_arr, 'last': string})

def config(request):

    return render(request, 'config.html')

def dmgr(request):
    ip = request.GET.get('add_ip', '')
    if ip != '':
        handle_ip_form(ip)
    try:
        if request.GET.get('remove'):
            remove = request.GET.get('remove')
            arr = get_pending_ip()
            entry = False
            for i in arr:
                if remove == i['IP']:
                    entry = i
            if entry is not False:
                arr.remove(entry)
            update_ip_form(arr)
    except:
        remove = ''
    data2json = dumps(get_pending_ip())
    return render(request, 'devMgr.html', {'data': data2json})
