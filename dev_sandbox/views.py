from django.shortcuts import render
from Packages.FormObjClass import *
from Packages.ViewRequestHandle import *

def sandbox(request, safe=True):
    if safe:
        if request.GET.get('user'):
            user = request.GET['user']
            data_dict = {'user': user}
            request_handle = ViewRequestHandler(user, 'sandbox')
            request_handle.get_request(request)
            '''if user is not False:
                if request.GET.get('filter'):
                    data_dict['filter'] = request.GET['filter']

                if request.GET.get('group'):
                    data_dict['group'] = request.GET['group']
                form = CreateForm('Sandbox')
                formObj = form.Analytics(data_dict)'''
            filter = request_handle.page_modifier_default['filter']
            return render(request, 'sandbox.html', request_handle.page_modifier)  #{'user': user, 'filter': filter})
        else:
            if request.POST.get('user'):
                user = request.POST['user']
                data_dict = {'user': user}
                if user is not False:
                    if request.GET.get('filter'):
                        data_dict['filter'] = request.GET['filter']

                    if request.GET.get('group'):
                        data_dict['group'] = request.GET['group']
                    form = CreateForm('Sandbox')
                    formObj = form.PrinterMonitor(data_dict)
                    return render(request, 'sandbox3.html', {'user': user, 'form': formObj})


'''class createForm(object):
    def __init__(self, site):
        self.formObj = {
            'divId': 'formId',
            'divClass': 'headInput',
            'formId': 'inputForm',
            'link': formObjDict[site]}
        self.inputObjects = []

class addTextInput(object):
    def __init__(self, label, value_name, value):
        self.object = {
        'objType': 'input',
        'objData': {
            'formId': 'inputForm',
            'width': '30%',
            'inLabelText': 'label',
            'inLabelClass': 'labelClass',
            'inId': 'inId',
            'inName': 'textname',
            'inClass': 'text',
            'inValue': 'lastValue'
            }
        }

formObj = {
    'divId': 'formId',
    'divClass': 'headInput',
    'formId': 'inputForm',
    'link': 'http://printerwatch/subsite/monitor/',
    'inputs': [{
        'objType': 'input',
        'objData': {
            'formId': 'inputForm',
            'width': '30%',
            'inLabelText': 'label :',
            'inLabelClass': 'labelClass',
            'inId': 'inId',
            'inName': 'textname',
            'inClass': 'text',
            'inValue': 'lastValue'
        }
    }, {
        'objType': 'hidden',
        'objData': {
            'formId': 'inputForm',
            'value': '123',
            'name': 'hiddenname'
        }
    }, {
        'objType': 'submit',
        'objData': {
            'formId': 'inputForm',
            'width': 'auto',
            'height': '100%',
            'subText': '>>'
        }
    }]}
''''''
formObj = {
    'divId': 'formId',
    'divClass': 'headInput',
    'formId': 'inputForm',
    'link': 'site.html',
    'inputs': [{
        'objType': 'select',
        'objData': {
            'formId': 'inputForm',
            'width': '30%',
            'selLabelText': 'label :',
            'selLabelClass': 'labelClass',
            'selId': 'selId',
            'selName': 'selname',
            'selClass': 'select',
            'selOptions': ['opt0', 'opt1', 'opt2']
        }
    }, {
        'objType': 'input',
        'objData': {
            'formId': 'inputForm',
            'width': '30%',
            'inLabelText': 'label :',
            'inLabelClass': 'labelClass',
            'inId': 'inId',
            'inName': 'textname',
            'inClass': 'text',
            'inValue': 'lastValue'
        }
    }, {
        'objType': 'hidden',
        'objData': {
            'formId': 'inputForm',
            'value': '123',
            'name': 'hiddenname'
        }
    }, {
        'objType': 'submit',
        'objData': {
            'formId': 'inputForm',
            'width': 'auto',
            'height': '100%',
            'subText': '>>'
        }
    }]}
'''