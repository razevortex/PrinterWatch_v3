import copy

from Packages.StrucData import CartStoreTracker
from Packages.SubPkg.csv_handles import LibOverride
from Packages.SubPkg.foos import dict_key_translate

formObjDict = {'PrinterMonitor': 'http://printerwatch/subsite/monitor/',
               'CartridgeStorage': 'http://printerwatch/subsite/storage_tracker/',
               'Sandbox': 'http://printerwatch/sandbox/',
               'Analytics': 'http://printerwatch/subsite/analytics/',
               'Details': 'http://printerwatch/subsite/details/',
               'DeviceManager': 'http://printerwatch/subsite/deviceMgr/',
               'UserMgr': 'http://printerwatch/subsite/userMgr/'}


def device_detail_form_obj(head, access):
    formObj = {
        'formId': 'detailOR',
        'access': access,
        'formAction': formObjDict['Details']}
    a = head['Device']
    b = head['IP']
    fixed = [a[0], b[0]]
    temp = {'fixed': fixed, 'editable': {'deviceId': head['Serial_No'], 'location': head['Location'], 'contact': head['Contact'], 'notes': head['Notes']},
         'inputIds': ['deviceId', 'location', 'contact', 'notes']}
    formObj.update(temp)
    return formObj


def ddf(head):
    device_details_key = [('deviceId', 'Serial_No'), ('location', 'Location'), ('contact', 'Contact'),
                          ('notes', 'Notes')]
    a = head['Device']
    b = head['IP']
    fixed = f'{a}  /  IP: {b}'
    temp = {'fixed': fixed}
    head_dup = copy.deepcopy(head)
    or_lib = LibOverride()
    or_lib.updateDict(head_dup)
    for key in head_dup.keys():
        if head_dup[key] == '':
            head_dup[key] = 'NaN'
    head = dict_key_translate(device_details_key, head, way=(1, 0))
    head_dup = dict_key_translate(device_details_key, head_dup, way=(1, 0))
    for key in ['deviceId', 'location', 'contact', 'notes']:
        label = f'{key}Label'
        temp[label] = head[key]
        temp[key] = head_dup[key] if temp[label] != head_dup[key] else ''
    temp['ID'] = temp['deviceIdLabel']
    return temp


class CreateForm(object):
    def __init__(self, site, form_Id='inputForm'):
        self.formObj = {
            'divId': 'formId',
            'divClass': 'form',
            'formId': form_Id,
            'link': formObjDict[site]}
        self.inputObjects = []


    def PrinterMonitor(self, data_dict):
        textInput = AddTextInput('Filter : ', 'filter', data_dict['filter'])
        self.inputObjects.append(textInput.object)
        submitButton = AddSubmitButton()
        self.inputObjects.append(submitButton.object)
        self.formObj['inputs'] = self.inputObjects
        return self.formObj


    def DeviceManager(self):
        textInput = AddTextInput('Add IP : ', 'add_ip', '')
        self.inputObjects.append(textInput.object)
        submitButton = AddSubmitButton()
        self.inputObjects.append(submitButton.object)
        self.formObj['inputs'] = self.inputObjects
        return self.formObj


    def CartStorage(self, data_dict):
        textInput = AddTextInput('Days : ', 'days', data_dict['days'])
        self.inputObjects.append(textInput.object)
        carts = CartStoreTracker()
        filter_mode_list = carts.list_of_cart_types()
        if 'filter_mode' not in list(data_dict.keys()):
            data_dict['filter_mode'] = 'Only changing'
        filter_mode_list.append('Only changing')
        filter_mode = AddSelectInput('Filter/Mode : ', 'filter_mode', filter_mode_list, data_dict['filter_mode'])
        self.inputObjects.append(filter_mode.object)

        submitButton = AddSubmitButton()
        self.inputObjects.append(submitButton.object)
        self.formObj['inputs'] = self.inputObjects
        return self.formObj


    def Analytics(self, dict):
        data_dict = {'group': 'Serial_No', 'value': 'BW', 'filter': ''}
        data_dict.update(dict)
        group_list = ['Serial_No', 'Manufacture', 'Model']
        value_list = ['BCYM', 'BW', 'CostPerBW', 'CostPerBCYM',
                      'PpBK', 'PpC', 'PpM', 'PpY', 'Total_BW',
                      'Total_BCYM', 'Total_Output']
        group_sel = AddSelectInput('Grouping : ', 'group', group_list, data_dict['group'], width='20%')
        self.inputObjects.append(group_sel.object)
        value_sel = AddSelectInput('Plot Val : ', 'value', value_list, data_dict['value'], width='20%')
        self.inputObjects.append(value_sel.object)
        filter_input = AddTextInput('Filter : ', 'filter', data_dict['filter'], width='30%')
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

    def AdminApplyUser(self, user_dict, u, sudo):
        for user in user_dict.keys():
            state_list = ['user', 'sudo']
            if user_dict[user] not in state_list:
                state_list.append(user_dict[user])
            if user_dict[user] == 'sudo':
                state_list = ['sudo']
                if u == user:
                    state_list.append('delete')
            elif sudo:
                state_list.append('delete')
            appling = AddSelectInput(user, user, state_list, user_dict[user], width='60%')
            self.inputObjects.append(appling.object)
        submit = AddSubmitButton()
        self.inputObjects.append(submit.object)
        for inputObj in self.inputObjects:
            t = inputObj['objData']
            t['formId'] = self.formObj['formId']
        self.formObj['inputs'] = self.inputObjects
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
        vl = copy.deepcopy(val_list)
        vl.remove(value)
        vl.insert(0, value)
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
            'selOptions': vl
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
