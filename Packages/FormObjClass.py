import copy

formObjDict = {'PrinterMonitor': 'http://printerwatch/subsite/monitor/',
               'CartridgeStorage': 'http://printerwatch/subsite/storage_tracker/',
               'Sandbox': 'http://printerwatch/sandbox/'}


class CreateForm(object):
    def __init__(self, site):
        self.formObj = {
            'divId': 'formId',
            'divClass': 'form',
            'formId': 'inputForm',
            'link': formObjDict[site]}
        self.inputObjects = []

    def PrinterMonitor(self, data_dict):
        textInput = AddTextInput('Filter : ', 'filter', data_dict['filter_value'])
        self.inputObjects.append(textInput.object)
        #hiddenInput = AddHiddenInput('test')
        #self.inputObjects.append(hiddenInput.object)
        submitButton = AddSubmitButton()
        self.inputObjects.append(submitButton.object)
        self.formObj['inputs'] = self.inputObjects
        return self.formObj

    def CartStorage(self, data_dict):
        textInput = AddTextInput('Track days : ', 'days', data_dict['days'])
        self.inputObjects.append(textInput.object)
        # hiddenInput = AddHiddenInput('test')
        # self.inputObjects.append(hiddenInput.object)
        submitButton = AddSubmitButton()
        self.inputObjects.append(submitButton.object)
        self.formObj['inputs'] = self.inputObjects
        return self.formObj

    def Analytics(self, dict):
        data_dict = {'group': 'Serial_No', 'value': 'BW', 'filter': ''}
        data_dict.update(dict)
        group_list = ['Serial_No', 'Manufacture', 'Model']
        value_list = ['BCYM', 'BW']
        group_sel = AddSelectInput('Grouping : ', 'group', group_list, data_dict['group'], width='20%')
        self.inputObjects.append(group_sel.object)
        value_sel = AddSelectInput('Plotted value : ', 'value', value_list, data_dict['value'], width='20%')
        self.inputObjects.append(value_sel.object)
        filter_input = AddTextInput('Filter : ', 'filter', data_dict['filter'], width='20%')
        self.inputObjects.append(filter_input.object)
        submitButton = AddSubmitButton()
        self.inputObjects.append(submitButton.object)
        self.formObj['inputs'] = self.inputObjects
        return self.formObj

    def DeviceDetails(self, dict):
        data_dict = {'time': 'total', 'vals': 'seperated'}
        data_dict.update(dict)
        time_list = ['total', 'daily', 'monthly']
        vals_list = ['seperated', 'grouped']
        time_sel = AddSelectInput('TimePeriode : ', 'time', time_list, data_dict['time'])
        self.inputObjects.append(time_sel)
        vals_sel = AddSelectInput('Toner : ', 'vals', vals_list, data_dict['vals'])
        self.inputObjects.append(vals_sel)
        submitButton = AddSubmitButton()
        self.inputObjects.append(submitButton.object)
        self.formObj['inputs'] = self.inputObjects
        formObj0 = copy.deepcopy(self.formObj)
        self.inputObjects = []
        override_this = ['Notes', 'Serial_No', 'Contact', 'Location']
        override = AddSelectInput('Override Value : ', 'override_this', override_this, 'Notes')
        self.inputObjects.append(override)
        with_value = AddTextInput('with : ', 'with', '')
        self.inputObjects.append(with_value)
        return self.formObj

class AddTextInput(object):
    def __init__(self, label, value_name, value, width='30%'):
        self.object = {
        'objType': 'input',
        'objData': {
            'formId': 'inputForm',
            'width': width,
            'inLabelText': label,
            'inLabelClass': 'labelClass',
            'inId': 'inId',
            'inName': value_name,
            'inClass': 'text',
            'inValue': value
            }
        }

class AddSelectInput(object):
    def __init__(self, label, name, val_list, value, width='30%'):
        val_list.remove(value)
        val_list.insert(0, value)
        self.object = {
        'objType': 'select',
        'objData': {
            'formId': 'inputForm',
            'width': width,
            'selLabelText': label,
            'selLabelClass': 'labelClass',
            'selId': name,
            'selName': name,
            'selClass': 'select',
            'selOptions': val_list
        }
    }

class AddHiddenInput(object):
    def __init__(self, value):
        self.object = {
        'objType': 'hidden',
        'objData': {
            'formId': 'inputForm',
            'inName': 'user',
            'inId': 'user',
            'inValue': value
        }
    }


class AddSubmitButton(object):
    def __init__(self):
        self.object = {
        'objType': 'submit',
        'objData': {
            'formId': 'inputForm',
            'width': 'auto',
            'height': '100%',
            'subText': '>>'
        }
    }

if __name__ == '__main__':
    data_dict = {'user': 'Raze', 'filter_value': 'test'}
    form = CreateForm('Sandbox')
    formObj = form.PrinterMonitor(data_dict)
    print(formObj)
