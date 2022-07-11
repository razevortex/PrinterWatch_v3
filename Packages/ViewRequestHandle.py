import copy
import datetime as dt
from django.http import HttpResponse, QueryDict
from Packages.SubPkg.const.ConstantParameter import page_modifier_dict_templates, data_modifier_dict_templates
from Packages.SubPkg.foos import read_conf, write_conf, data_view_request_CartStorage, dict_key_translate, handle_ip_form, remove_ip
from Packages.SubPkg.csv_handles import LibOverride, Logging


device_details_key = [('ID', 'ID'), ('deviceId', 'Serial_No'), ('location', 'Location'), ('contact', 'Contact'), ('notes', 'Notes')]


class ViewRequestHandler(object):
    def __init__(self, user, view_page, data_mod=False, sudo=False):
        # a true sudo val is needed to have permission to make changes
        self.sudo = sudo
        # get the basic values needed like the actual page user and the expected values
        self.user = user
        self.view_page = view_page
        # the expected values are stored in a dict in ConstantParameter.py
        self.page_modifier_default = page_modifier_dict_templates[view_page]
        # exclude the DeviceManager from gather last used values
        if self.view_page != 'DeviceManager':
            self.page_modifier = read_conf(self.user, view_page)
        # data_modifier only used on some pages hand handle respons values that make some
        # changes to or will create stored values in cartStorage.txt, override.csv, includeIP.txt
        # all these inputs should get logged with user time and input information
        self.data_modifier_default = False
        self.data_modifier = {}
        self.debug = 'val = '
        if view_page in data_modifier_dict_templates.keys():
            self.data_modifier_default = data_modifier_dict_templates[view_page]
        if data_mod is not False:
            self.data_modifier_default['ID'] = data_mod['deviceIdLabel']
        self.log_entry = {'User': self.user, 'Page': self.view_page}

    def get_request(self, request_obj):
        t_get_dic = request_obj.GET.copy()
        if self.view_page != 'DeviceManager':
            # loop to get GET for page modifier values
            for get_key, value in self.page_modifier_default.items():
                if t_get_dic.get(get_key, value):
                    self.page_modifier[get_key] = t_get_dic.get(get_key, value)
            # store changes to users last used values
            write_conf(self.user, self.view_page, self.page_modifier)
            self.page_modifier['user'] = self.user
        if self.sudo:
            if self.view_page == 'DeviceDetails':
                self.DeviceOR(t_get_dic)
                return
            elif self.view_page == 'DeviceManager':
                try:
                    handle_ip_form(self.data_modifier['add_ip'])
                except:
                    try:
                        remove_ip(self.data_modifier['remove'])
                    except:
                        return
            elif self.view_page == 'CartStorage':
                self.debug = ''
                modified = True
                for get_key, value in data_modifier_dict_templates[self.view_page].items():
                    if t_get_dic.get(get_key, value):
                        self.data_modifier_default[get_key] = t_get_dic.get(get_key, value)
                        if self.data_modifier_default[get_key] is not False:
                            self.debug += f'{self.user} time: {str(dt.datetime.now())}: {get_key} -> {t_get_dic.get(get_key, value)}'
                    else:
                        modified = False
                if modified:
                    self.log_entry['Data'] = str(self.data_modifier_default)
                    log = Logging()
                    log.newLogEntry(self.log_entry)
                data_view_request_CartStorage(self.data_modifier_default)
                return

    def DeviceOR(self, t_get_dic):
        self.data_modifier_default = dict_key_translate(device_details_key, self.data_modifier_default, way=(0, 1))
        dbOR = LibOverride()
        self.data_modifier_default = dbOR.orDict(self.data_modifier_default)
        self.data_modifier_default = dict_key_translate(device_details_key, self.data_modifier_default, way=(1, 0))
        string = f'{self.user} time: {str(dt.datetime.now())}: '
        modified = False
        for get_key, value in data_modifier_dict_templates[self.view_page].items():
            if t_get_dic.get(get_key, value):
                if self.data_modifier_default[get_key] != t_get_dic.get(get_key, value):
                    string += f' {get_key} -> {t_get_dic.get(get_key, value)} | '
                    modified = True
                self.data_modifier_default[get_key] = t_get_dic.get(get_key, value)
                self.debug += string
        if modified is not False:
            self.log_entry['Data'] = str(self.data_modifier_default)
            log = Logging()
            log.newLogEntry(self.log_entry)
            #dbOR.log_changes(self.user, self.data_modifier_default)
        self.data_modifier_default = dict_key_translate(device_details_key, self.data_modifier_default, way=(0, 1))
        dbOR.dataToDb(self.data_modifier_default['ID'], self.data_modifier_default)

    def CartStoreDays(self):
        got = str(self.page_modifier['days'])
        if '.' in got:
            now = dt.date.today()
            date_tup = got.split('.')
            date_tup = date_tup[::-1]
            y, m, d = (date_tup[0], date_tup[1], date_tup[2])
            print(y, m, d)
            ts = dt.date(year=int(y), month=int(m), day=int(d))
            delta = ts - now
            return delta.days
        return self.page_modifier['days']



