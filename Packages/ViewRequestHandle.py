import copy
import datetime as dt
from django.http import HttpResponse, QueryDict
from Packages.SubPkg.const.ConstantParameter import page_modifier_dict_templates, data_modifier_dict_templates
from Packages.SubPkg.foos import read_conf, write_conf, data_view_request_CartStorage, dict_key_translate
from Packages.SubPkg.csv_handles import LibOverride


device_details_key = [('ID', 'ID'), ('deviceId', 'Serial_No'), ('location', 'Location'), ('contact', 'Contact'), ('notes', 'Notes')]


class ViewRequestHandler(object):
    def __init__(self, user, view_page, data_mod=False):
        self.user = user
        self.view_page = view_page
        self.page_modifier_default = page_modifier_dict_templates[view_page]
        self.page_modifier = read_conf(self.user, view_page)
        self.data_modifier_default = False
        self.data_modifier = {}
        self.debug = 'val = '
        if data_mod is not False:
            if type(data_mod) == dict:
                id = data_mod['Serial_No']
                id = id[0]
                t_dic = {'ID': id}
                for key, val in data_mod.items():
                    t_dic[key] = val[1]

                self.data_modifier_default = data_modifier_dict_templates['DeviceDetails']
                '''                    {'ID': id, 'deviceId': t_dic['Serial_No'],
                                              'location': t_dic['Location'],
                                              'contact': t_dic['Contact'],
                                              'notes': t_dic['Notes']}'''
                self.data_modifier = dict_key_translate(device_details_key, t_dic, way=(1, 0))
        else:
            if view_page in data_modifier_dict_templates.keys():
                self.data_modifier_default = data_modifier_dict_templates[view_page]

    def get_request(self, request_obj):
        t_get_dic = request_obj.GET.copy()
        # loop to get GET for page modifier
        for get_key, value in self.page_modifier_default.items():
            if t_get_dic.get(get_key, value):
                self.page_modifier[get_key] = t_get_dic.get(get_key, value)
        # store changes for user
        write_conf(self.user, self.view_page, self.page_modifier)
        self.page_modifier['user'] = self.user

        if self.data_modifier_default:
            # loop to get GET for data modifier
            for get_key, value in self.data_modifier_default.items():
                self.debug += f'{get_key}:{t_get_dic.get(get_key, value)},'
                if t_get_dic.get(get_key, value):

                    self.data_modifier[get_key] = t_get_dic.get(get_key, value)
            if self.view_page == 'CartStorage':
                data_view_request_CartStorage(self.data_modifier)
            if self.view_page == 'DeviceDetails':
                #for key, val in self.data_modifier.items():


                #if self.data_modifier_default != self.data_modifier:
                dbOR = LibOverride()
                dbOR.updateDB(dict_key_translate(device_details_key, self.data_modifier, way=(0, 1)), self.data_modifier['ID'])


