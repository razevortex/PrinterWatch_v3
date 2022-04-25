import os

_HERE = os.path.realpath(__file__)
temp = _HERE.split(r'Packages')
# ROOT stores the absolute path to the project directory with \ at its end
ROOT = temp[0]#'/home/razevortex/PycharmProjects/pythonProject/PrinterWatch-webserver/PrinterWatch'
# example : 'D:\pypro\PrinterWatch2.1.1\'

# the header dict stores the csv/dict keys of each file/dict as list
header = {'request_db': ['TonerBK', 'TonerC', 'TonerM', 'TonerY',
                         'Printed_BW', 'Printed_BCYM', 'Copied_BW', 'Copied_BCYM',
                         'Status_Report', 'Time_Stamp'],
          'client_db': ['Serial_No', 'IP', 'Manufacture', 'Model', 'Time_Stamp'],
          'client_specs': ['Serial_No', 'CartBK', 'CartC', 'CartM', 'CartY', 'Location', 'Contact', 'Notes'],
          'model_specs': ['Model', 'Color', 'Scanner', 'Cart', 'MethodIndex'],
          'data_table': ['Serial_No', 'IP', 'Manufacture', 'Model', 'TonerBK', 'TonerC', 'TonerM', 'TonerY',
                         'Printed_BW', 'Printed_BCYM', 'Copied_BW', 'Copied_BCYM', 'Status_Report', 'Time_Stamp',
                         'CartBK', 'CartC', 'CartM', 'CartY', 'Location', 'Contact', 'Notes'],
          'config': ['Config_ID', 'data_table_displayed', 'Sort_Key'],
          'override': ['ID', 'Serial_No', 'CartBK', 'CartC', 'CartM', 'CartY', 'Location', 'Contact', 'Notes'],
          'statistics': ['Serial_No', 'IP', 'Manufacture', 'Model', 'CostBK', 'CostCYM', 'UsedBK', 'UsedCYM',
                         'PagesBK', 'PagesCYM', 'PagesPerBK', 'PagesPerCYM', 'DaysTotal',
                         'UsedBK_daily', 'UsedCYM_daily', 'PagesBK_daily', 'PagesCYM_daily', 'CostPerBK', 'CostPerCYM'],
          'statistics_group': ['Model', 'num', 'CostBK', 'CostCYM', 'UsedBK', 'UsedCYM', 'PagesBK', 'PagesCYM',
                               'UsedBK_daily', 'UsedCYM_daily', 'PagesBK_daily', 'PagesCYM_daily', 'CostPerBK',
                               'CostPerCYM', 'PagesPerBK', 'PagesPerCYM'],
          'ext': ['CostBK', 'CostCYM', 'UsedBK', 'UsedCYM',
                         'PagesBK', 'PagesCYM', 'PagesPerBK', 'PagesPerCYM', 'DaysTotal',
                         'UsedBK_daily', 'UsedCYM_daily', 'PagesBK_daily', 'PagesCYM_daily', 'CostPerBK', 'CostPerCYM'],
          'recentCached': ['Serial_No', 'Device', 'IP', 'Contact', 'Location', 'Carts', 'UsedBK_daily', 'UsedCYM_daily',
                           'PagesBK_daily', 'PagesCYM_daily', 'CostPerBK', 'CostPerCYM', 'TonerBK', 'TonerC', 'TonerM',
                           'TonerY', 'Printed_BW', 'Printed_BCYM', 'Copied_BW', 'Copied_BCYM', 'Status_Report', 'Time_Stamp', 'ID']
          }

stat_header = {'client_stats': ['Serial_No', 'Device', 'DaysMonitored', 'TonerYPerDay', 'PpY', 'BCYMPerDay',
                                'CostPerBCYM', 'PpC', 'TonerBKPerDay', 'PpBK',
                                'PpM', 'CostPerBW', 'TonerCPerDay', 'TonerMPerDay', 'BWPerDay'],
               'device_stats': ['Device', '#', 'DaysMonitored', 'TonerYPerDay', 'PpY', 'BCYMPerDay', 'CostPerBCYM',
                                'PpC', 'TonerBKPerDay', 'PpBK', 'PpM', 'CostPerBW', 'TonerCPerDay', 'TonerMPerDay',
                                'BWPerDay']}

statistics_key_type = {'Serial_No': 'string', 'IP': 'string', 'Manufacture': 'string', 'Model': 'string',
                       'CostBK': 'float', 'CostCYM': 'float',
                       'UsedBK': 'int', 'UsedCYM': 'int', 'PagesBK': 'int', 'PagesCYM': 'int', 'PagesPerBK': 'float',
                       'PagesPerCYM': 'float', 'DaysTotal': 'int', 'UsedBK_daily': 'float', 'UsedCYM_daily': 'float',
                       'PagesBK_daily': 'float', 'PagesCYM_daily': 'float', 'CostPerBK': 'float', 'CostPerCYM': 'float'}

statistics_grouping_vals = ['PagesPerBK', 'PagesPerCYM', 'UsedBK_daily', 'UsedCYM_daily',
                              'PagesBK_daily', 'PagesCYM_daily', 'CostPerBK', 'CostPerCYM']

statistics_grouping_dict = {'PagesPerBK': [], 'PagesPerCYM': [], 'UsedBK_daily': [], 'UsedCYM_daily': [],
                            'PagesBK_daily': [], 'PagesCYM_daily': [], 'CostPerBK': [], 'CostPerCYM': []}

# kyocera mib list index´s 0 = Max, 1 = Fill, 2 = Cart
kyocera_color_toner_mib = [{'TonerC': 'mib-2.43.11.1.1.8.1.1', 'TonerM': 'mib-2.43.11.1.1.8.1.2',
                            'TonerY': 'mib-2.43.11.1.1.8.1.3', 'TonerBK': 'mib-2.43.11.1.1.8.1.4'},
                           {'TonerC': 'mib-2.43.11.1.1.9.1.1', 'TonerM': 'mib-2.43.11.1.1.9.1.2',
                            'TonerY': 'mib-2.43.11.1.1.9.1.3', 'TonerBK': 'mib-2.43.11.1.1.9.1.4'},
                           {'CartC': 'mib-2.43.11.1.1.6.1.1', 'CartM': 'mib-2.43.11.1.1.6.1.2',
                            'CartY': 'mib-2.43.11.1.1.6.1.3', 'CartBK': 'mib-2.43.11.1.1.6.1.4'}]

kyocera_color_mib_ecosys = {'Printed_BW': 'enterprises.1347.42.3.1.2.1.1.1.1',
                            'Printed_BCYM': 'enterprises.1347.42.3.1.2.1.1.1.2',
                            'Copied_BW': 'enterprises.1347.42.3.1.2.1.1.2.1',
                            'Copied_BCYM': 'enterprises.1347.42.3.1.2.1.1.2.2',
                            'Status_Report': 'enterprises.1347.43.18.2.1.2.1.1',
                            'Contact': 'sysContact.0', 'Location': 'sysLocation.0'}
kyocera_color_mib_taskalfa = {'Printed_BW': 'enterprises.1347.42.3.1.2.1.1.1.1',
                              'Printed_BCYM': 'enterprises.1347.42.3.1.2.1.1.1.3',
                              'Copied_BW': 'enterprises.1347.42.3.1.2.1.1.2.1',
                              'Copied_BCYM': 'enterprises.1347.42.3.1.2.1.1.2.3',
                              'Status_Report': 'enterprises.1347.43.18.2.1.2.1.1',
                              'Contact': 'sysContact.0', 'Location': 'sysLocation.0'}

kyocera_bw_toner_mib = [{'TonerBK': 'mib-2.43.11.1.1.8.1.1'},
                        {'TonerBK': 'mib-2.43.11.1.1.9.1.1'},
                        {'CartBK': 'mib-2.43.11.1.1.6.1.1'}]

kyocera_bw_mib = {'Printed_BW': 'enterprises.1347.42.3.1.1.1.1.1',
                  'Copied_BW': 'enterprises.1347.42.3.1.1.1.1.2',
                  'Status_Report': 'enterprises.1347.43.18.2.1.2.1.1',
                  'Contact': 'sysContact.0', 'Location': 'sysLocation.0'}
kyocera_bw_mib_fs1320d = {'Printed_BW': 'enterprises.1347.42.3.1.1.1.1.1',
                          'Copied_BW': 'enterprises.1347.42.3.1.1.1.1.2',
                          'Status_Report': 'enterprises.1347.43.18.2.1.2.1.1',
                          'Contact': 'sysContact.0', 'Location': 'sysLocation.0'}
kyocera_color_keys_ecosys = []
for d in kyocera_color_toner_mib:
    for keys, vals in d.items():
        kyocera_color_keys_ecosys.append(vals)
for keys, vals in kyocera_color_mib_ecosys.items():
    kyocera_color_keys_ecosys.append(vals)

kyocera_color_keys_taskalfa = []
for d in kyocera_color_toner_mib:
    for keys, vals in d.items():
        kyocera_color_keys_taskalfa.append(vals)
for keys, vals in kyocera_color_mib_taskalfa.items():
    kyocera_color_keys_taskalfa.append(vals)

kyocera_bw_keys_fs1320d = []
for d in kyocera_bw_toner_mib:
    for keys, vals in d.items():
        kyocera_bw_keys_fs1320d.append(vals)
for keys, vals in kyocera_bw_mib.items():
    kyocera_bw_keys_fs1320d.append(vals)

kyocera_bw_keys = []
for d in kyocera_bw_toner_mib:
    for keys, vals in d.items():
        kyocera_bw_keys.append(vals)
for keys, vals in kyocera_bw_mib.items():
    kyocera_bw_keys.append(vals)

kyocera_snmp_batch_oids = ['1.3.6.1.2.1.43.11',  # oid part for all the toner values
                           '1.3.6.1.4.1.1347.42.3.1',  # oid part for all the Page counter
                           '1.3.6.1.4.1.1347.43.18.2.1.2.1.1',  # oid part for status monitor
                           '1.3.6.1.2'  # base walk for location and contact i would like to have a more specific oid
                           # but did not find a working one yet
                           ]


# the data_dict_template creates an empty dict that gets filled with the gathered client data and then updated in a list
# of all these dicts from the clients the gui table pulls its data out of this list
def data_dict_template():
    data_dict_temp = {}
    for val in header['data_table']:
        data_dict_temp[val] = 'NaN'
    return data_dict_temp


# error_code is not implemented yet but is planed to store certain outputs
# of common occuring errors for helping with debugging
error_code = ['csv_handles 404 no matching key was found',
              'csv_handles the entry tryed to add didnt had the expected amount of values']

# this group of lists/dicts is used by the RequestHandle.ClientGet initiating the request and gathering the data
# needed to identify the method used for the request
ManufacturerList = ['KYOCERA', 'Brother']
translate_Kyocera = {'Manufacture': 'Kyocera', '2.43.5.1.1.16.1': 'Model', '2.43.5.1.1.17.1': 'Serial_No'}
translate_Brother = {'Manufacture': 'Brother', 'hrDeviceDescr.1': 'Model', '2.43.5.1.1.17.1': 'Serial_No'}
mib_head_snmp = {'Kyocera': translate_Kyocera, 'Brother': translate_Brother}

plot_value_lists = {'single_client_statistic': ['Printed_BW', 'Copied_BW', 'Printed_BCYM', 'Copied_BCYM',
                                                'TonerBK', 'TonerC', 'TonerM', 'TonerY']}

TONER_COST_DICT = {'TN-2000': ('57,61 €', 57.61), 'TN-3030': ('59,78 €', 59.78), 'TN-3060': ('81,24 €', 81.24),
                   'TN-3130': ('68,17 €', 68.17), 'TN-3170': ('91,32 €', 91.32), 'TN-3230': ('59,52 €', 59.52),
                   'TN-3280': ('98,20 €', 98.2), 'TN-3280TWIN': ('194,01 €', 194.01), 'TN-3330': ('59,99 €', 59.99),
                   'TN-3380': ('94,34 €', 94.34), 'TN-3380TWIN': ('189,07 €', 189.07), 'TN-3390': ('106,21 €', 106.21),
                   'TN-242BK': ('50,17 €', 50.17), 'TN-246C': ('70,40 €', 70.4), 'TN-242C': ('50,02 €', 50.02),
                   'TN-246M': ('70,17 €', 70.17), 'TN-242M': ('49,67 €', 49.67), 'TN-246Y': ('70,21 €', 70.21),
                   'TN-242Y': ('49,46 €', 49.46), 'TN-241BK': ('49,93 €', 49.93), 'TN-241C': ('49,89 €', 49.89),
                   'TN-245BK': ('49,93 €', 49.93), 'TN-246BK': ('50,17 €', 50.17),
                   'TN-245C': ('70,55 €', 70.55), 'TN-241M': ('49,42 €', 49.42), 'TN-245M': ('70,78 €', 70.78),
                   'TN-241Y': ('49,50 €', 49.5), 'TN-245Y': ('70,63 €', 70.63), 'TN-130BK': ('47,48 €', 47.48),
                   'TN-135BK': ('64,82 €', 64.82), 'TN-130C': ('62,86 €', 62.86), 'TN-130M': ('62,86 €', 62.86),
                   'TN-130Y': ('62,86 €', 62.86), 'TN-135Y': ('116,53 €', 116.53), 'TN-320BK': ('44,04 €', 44.04),
                   'TN-325BK': ('50,28 €', 50.28), 'TN-325C': ('103,79 €', 103.79), 'TN-320C': ('58,76 €', 58.76),
                   'TN-325M': ('105,16 €', 105.16), 'TN-320M': ('59,65 €', 59.65), 'TN-325Y': ('103,96 €', 103.96),
                   'TN-320Y': ('58,76 €', 58.76), 'TN-328BK': ('64,65 €', 64.65), 'TN-328C': ('143,48 €', 143.48),
                   'TN-328M': ('143,18 €', 143.18), 'TN-328Y': ('143,18 €', 143.18), 'TN-243BK': ('37,24 €', 37.24),
                   'TN-247BK': ('64,03 €', 64.03), 'TN-243C': ('40,86 €', 40.86), 'TN-247C': ('73,82 €', 73.82),
                   'TN-243M': ('40,63 €', 40.63), 'TN-247M': ('73,91 €', 73.91), 'TN-243CMYK': ('135,39 €', 135.39),
                   'TN-243Y': ('40,85 €', 40.85), 'TN-247Y': ('74,09 €', 74.09), 'TN-3430': ('57,35 €', 57.35),
                   'TN-3480': ('96,76 €', 96.76), 'TN-3512': ('109,08 €', 109.08), 'TN-421BK': ('72,49 €', 72.49),
                   'TN-423BK': ('83,83 €', 83.83), 'TN-421C': ('63,84 €', 63.84), 'TN-423C': ('111,77 €', 111.77),
                   'TN-421M': ('63,84 €', 63.84), 'TN-423M': ('112,62 €', 112.62), 'TN-421Y': ('63,26 €', 63.26),
                   'TN-423Y': ('111,77 €', 111.77), 'TN-200': ('29,75 €', 29.75), 'TN-8000': ('32,72 €', 32.72),
                   'TN-6600': ('88,91 €', 88.91), 'TN-6300': ('63,53 €', 63.53), 'TN-1050': ('29,92 €', 29.92),
                   'TN-2005': ('40,28 €', 40.28), 'TN-2010': ('27,05 €', 27.05), 'TN-2110': ('37,52 €', 37.52),
                   'TN-2120': ('54,75 €', 54.75), 'TN-2220': ('48,70 €', 48.7), 'TN-2210': ('31,64 €', 31.64),
                   'TN-230BK': ('52,75 €', 52.75), 'TN-230C': ('50,55 €', 50.55), 'TN-230M': ('51,17 €', 51.17),
                   'TN-230Y': ('50,91 €', 50.91), 'TN-4100': ('88,01 €', 88.01), 'TN-5500': ('100,13 €', 100.13),
                   'TN-2310': ('32,77 €', 32.77), 'TN-2320': ('50,65 €', 50.65), 'TN-2420': ('58,58 €', 58.58),
                   'TN-2410': ('33,21 €', 33.21), 'TN-3520': ('137,46 €', 137.46), 'TN-321BK': ('47,43 €', 47.43),
                   'TN-321C': ('62,80 €', 62.8), 'TN-321M': ('61,96 €', 61.96), 'TN-321Y': ('62,25 €', 62.25),
                   'TN-326BK': ('50,46 €', 50.46), 'TN-326C': ('104,09 €', 104.09), 'TN-326M': ('104,82 €', 104.82),
                   'TN-326Y': ('105,36 €', 105.36), 'TN-329BK': ('65,38 €', 65.38), 'TN-329C': ('145,98 €', 145.98),
                   'TN-329M': ('148,21 €', 148.21), 'TN-329Y': ('147,76 €', 147.76), 'TN-426BK': ('90,91 €', 90.91),
                   'TN-426C': ('167,21 €', 167.21), 'TN-426M': ('166,15 €', 166.15), 'TN-426Y': ('168,68 €', 168.68),
                   'TN-900BK': ('60,26 €', 60.26), 'TN-900C': ('130,03 €', 130.03), 'TN-900M': ('129,00 €', 129.0),
                   'TN-900Y': ('129,00 €', 129.0), 'TN-910BK': ('83,91 €', 83.91), 'TN-910C': ('208,09 €', 208.09),
                   'TN-910M': ('208,72 €', 208.72), 'TN-910Y': ('210,20 €', 210.2), 'TK-3060': ('78,38 €', 78.38),
                   'TK-6115': ('81,89 €', 81.89), 'TK-5240K': ('50,52 €', 50.52), 'TK-5240C': ('73,17 €', 73.17),
                   'TK-5240M': ('73,57 €', 73.57), 'TK-5240Y': ('72,11 €', 72.11), 'TK-5280K': ('135,46 €', 135.46),
                   'TK-5280C': ('173,17 €', 173.17), 'TK-5280M': ('171,46 €', 171.46), 'TK-5280Y': ('174,06 €', 174.06),
                   'TK-5280CS': ('173,17 €', 173.17), 'TK-5280MS': ('171,46 €', 171.46),
                   'TK-5280YS': ('174,06 €', 174.06),
                   'TK-5140K': ('83,84 €', 83.84), 'TK-5140C': ('95,32 €', 95.32), 'TK-5140M': ('95,81 €', 95.81),
                   'TK-5140Y': ('95,06 €', 95.06), 'TK-8115K': ('62,53 €', 62.53), 'TK-8115C': ('57,76 €', 57.76),
                   'TK-8115M': ('57,31 €', 57.31), 'TK-8115Y': ('57,66 €', 57.66), 'TK-3160': ('81,10 €', 81.1),
                   'TK-3170': ('84,42 €', 84.42), 'TK-3190': ('107,23 €', 107.23), 'TK-7300': ('82,92 €', 82.92),
                   'TK-7310': ('80,68 €', 80.68), 'TK-5160K': ('127,51 €', 127.51), 'TK-5160C': ('134,98 €', 134.98),
                   'TK-5160M': ('133,62 €', 133.62), 'TK-5160Y': ('134,67 €', 134.67), 'TK-5290K': ('131,89 €', 131.89),
                   'TK-5290C': ('145,94 €', 145.94), 'TK-5290M': ('145,94 €', 145.94), 'TK-5290Y': ('146,31 €', 146.31),
                   'TK-1130': ('61,32 €', 61.32), 'TK-1140': ('75,37 €', 75.37), 'TK-1115': ('54,83 €', 54.83),
                   'TK-1125': ('47,66 €', 47.66), 'TK-140': ('76,42 €', 76.42), 'TK-160': ('51,65 €', 51.65),
                   'TK-25': ('88,45 €', 88.45), 'TK-130': ('95,23 €', 95.23), 'TK-170': ('87,14 €', 87.14),
                   'TK-310': ('104,49 €', 104.49), 'TK-340': ('92,32 €', 92.32), 'TK-3100': ('81,14 €', 81.14),
                   'TK-65': ('154,62 €', 154.62), 'TK-320': ('95,16 €', 95.16), 'TK-350': ('88,68 €', 88.68),
                   'TK-360': ('95,54 €', 95.54), 'TK-3110': ('96,26 €', 96.26), 'TK-3130': ('109,55 €', 109.55),
                   'TK-500C': ('134,89 €', 134.89), 'TK-500Y': ('134,89 €', 134.89), 'TK-400': ('123,10 €', 123.1),
                   'TK-475': ('79,30 €', 79.3), 'TK-440': ('84,24 €', 84.24), 'TK-450': ('92,34 €', 92.34),
                   'TK-110': ('84,68 €', 84.68), 'TK-70': ('157,96 €', 157.96), 'TK-710': ('138,15 €', 138.15),
                   'TK-150K': ('139,26 €', 139.26), 'TK-150C': ('181,24 €', 181.24), 'TK-150M': ('181,24 €', 181.24),
                   'TK-150Y': ('181,24 €', 181.24), 'TK-590K': ('83,65 €', 83.65), 'TK-590C': ('95,38 €', 95.38),
                   'TK-590M': ('95,38 €', 95.38), 'TK-590Y': ('95,32 €', 95.32), 'TK-520C': ('102,48 €', 102.48),
                   'TK-540K': ('82,04 €', 82.04), 'TK-540C': ('117,14 €', 117.14), 'TK-580K': ('44,37 €', 44.37),
                   'TK-580C': ('69,72 €', 69.72), 'TK-580M': ('70,38 €', 70.38), 'TK-580Y': ('70,38 €', 70.38),
                   'TK-550K': ('99,72 €', 99.72), 'TK-560K': ('129,89 €', 129.89), 'TK-560C': ('158,11 €', 158.11),
                   'TK-560M': ('165,05 €', 165.05), 'TK-560Y': ('145,63 €', 145.63), 'TK-570K': ('136,91 €', 136.91),
                   'TK-570C': ('148,59 €', 148.59), 'TK-570M': ('148,59 €', 148.59), 'TK-570Y': ('148,59 €', 148.59),
                   'TK-895K': ('62,45 €', 62.45), 'TK-895C': ('57,09 €', 57.09), 'TK-895M': ('58,22 €', 58.22),
                   'TK-895Y': ('57,26 €', 57.26), 'TK-820K': ('111,44 €', 111.44), 'TK-820C': ('104,80 €', 104.8),
                   'TK-820M': ('104,80 €', 104.8), 'TK-820Y': ('104,80 €', 104.8), 'TK-8600K': ('192,70 €', 192.7),
                   'TK-8600C': ('252,02 €', 252.02), 'TK-8600M': ('252,02 €', 252.02), 'TK-8600Y': ('252,02 €', 252.02),
                   'TK-100': ('45,75 €', 45.75), 'TK-410': ('49,61 €', 49.61), 'TK-420': ('59,74 €', 59.74),
                   'TK-675': ('84,69 €', 84.69), 'TK-715': ('115,25 €', 115.25), 'TK-825K': ('55,46 €', 55.46),
                   'TK-825C': ('75,61 €', 75.61), 'TK-825M': ('75,61 €', 75.61), 'TK-825Y': ('75,61 €', 75.61),
                   'TK-805C': ('119,70 €', 119.7), 'TK-805M': ('119,70 €', 119.7), 'TK-1170': ('71,26 €', 71.26),
                   'TK-1150': ('58,99 €', 58.99), 'TK-3150': ('77,76 €', 77.76), 'TK-5220K': ('42,46 €', 42.46),
                   'TK-5220C': ('52,53 €', 52.53), 'TK-5220M': ('52,29 €', 52.29), 'TK-5220Y': ('52,68 €', 52.68),
                   'TK-5150K': ('124,77 €', 124.77), 'TK-5150C': ('161,73 €', 161.73), 'TK-5150M': ('158,31 €', 158.31),
                   'TK-5150Y': ('157,89 €', 157.89), 'TK-1160': ('81,47 €', 81.47), 'TK-3200': ('147,25 €', 147.25),
                   'TK-5230K': ('52,20 €', 52.2), 'TK-5230C': ('78,76 €', 78.76), 'TK-5230M': ('75,46 €', 75.46),
                   'TK-5230Y': ('76,32 €', 76.32), 'TK-5270K': ('95,82 €', 95.82), 'TK-5270C': ('114,35 €', 114.35),
                   'TK-5270M': ('114,35 €', 114.35), 'TK-5270Y': ('114,35 €', 114.35), 'TK-8800K': ('196,34 €', 196.34),
                   'TK-8800C': ('254,98 €', 254.98), 'TK-8800M': ('254,98 €', 254.98), 'TK-8800Y': ('254,98 €', 254.98),
                   'TK-865K': ('71,99 €', 71.99), 'TK-865C': ('90,12 €', 90.12), 'TK-865M': ('90,12 €', 90.12),
                   'TK-865Y': ('90,12 €', 90.12), 'TK-8315K': ('39,90 €', 39.9), 'TK-8315C': ('41,58 €', 41.58),
                   'TK-8315M': ('41,58 €', 41.58), 'TK-8315Y': ('38,60 €', 38.6), 'TK-8325K': ('55,30 €', 55.3),
                   'TK-8325C': ('76,95 €', 76.95), 'TK-8325M': ('76,95 €', 76.95), 'TK-8325Y': ('76,89 €', 76.89),
                   'TK-8345K': ('48,14 €', 48.14), 'TK-8345C': ('75,34 €', 75.34), 'TK-8345M': ('75,41 €', 75.41),
                   'TK-8345Y': ('75,29 €', 75.29), 'TK-5135K': ('67,72 €', 67.72), 'TK-5135C': ('65,67 €', 65.67),
                   'TK-5135M': ('65,67 €', 65.67), 'TK-5135Y': ('65,67 €', 65.67), 'TK-685': ('68,30 €', 68.3),
                   'TK-7105': ('74,30 €', 74.3), 'TK-8305K': ('65,78 €', 65.78), 'TK-8305C': ('94,78 €', 94.78),
                   'TK-8305M': ('94,83 €', 94.83), 'TK-8305Y': ('94,83 €', 94.83), 'TK-8505K': ('81,41 €', 81.41),
                   'TK-8505C': ('122,23 €', 122.23), 'TK-8505M': ('122,23 €', 122.23), 'TK-8505Y': ('122,23 €', 122.23),
                   'TK-5195K': ('53,08 €', 53.08), 'TK-5195C': ('90,81 €', 90.81), 'TK-5195M': ('90,81 €', 90.81),
                   'TK-5195Y': ('90,81 €', 90.81), 'TK-8335K': ('52,33 €', 52.33), 'TK-8335C': ('90,28 €', 90.28),
                   'TK-8335M': ('87,91 €', 87.91), 'TK-8335Y': ('90,28 €', 90.28), 'TK-5305K': ('62,54 €', 62.54),
                   'TK-5305C': ('82,54 €', 82.54), 'TK-5305M': ('82,54 €', 82.54), 'TK-5305Y': ('82,54 €', 82.54),
                   'TK-6305': ('107,61 €', 107.61), 'TK-5345K': ('57,63 €', 57.63), 'TK-5345C': ('116,49 €', 116.49),
                   'TK-5345M': ('117,04 €', 117.04), 'TK-5345Y': ('112,26 €', 112.26), 'TK-8375K': ('62,71 €', 62.71),
                   'TK-8375C': ('117,13 €', 117.13), 'TK-8375M': ('117,13 €', 117.13), 'TK-8375Y': ('117,13 €', 117.13),
                   'TK-6325': ('99,71 €', 99.71), 'TK-7225': ('123,09 €', 123.09), 'TK-8525K': ('56,74 €', 56.74),
                   'TK-8525C': ('116,10 €', 116.1), 'TK-8525M': ('115,81 €', 115.81), 'TK-8525Y': ('118,92 €', 118.92),
                   'TK-5215K': ('42,99 €', 42.99), 'TK-5215C': ('101,80 €', 101.8), 'TK-5215M': ('101,80 €', 101.8),
                   'TK-5215Y': ('101,80 €', 101.8), 'TK-8515K': ('55,25 €', 55.25), 'TK-8515C': ('112,04 €', 112.04),
                   'TK-8515M': ('112,04 €', 112.04), 'TK-8515Y': ('112,04 €', 112.04), 'TK-8705K': ('185,29 €', 185.29),
                   'TK-8705C': ('169,62 €', 169.62), 'TK-8705M': ('169,62 €', 169.62), 'TK-8705Y': ('176,31 €', 176.31),
                   'TK-8725K': ('101,81 €', 101.81), 'TK-8725C': ('179,88 €', 179.88), 'TK-8725M': ('179,88 €', 179.88),
                   'TK-8725Y': ('179,88 €', 179.88), 'TK-435': ('66,81 €', 66.81), 'TK-6325K': ('99,71 €', 99.71)}
statistics_variable_grouping_method = {'single_val': ['CostBK', 'CostCYM'],
                                       'sum_val': ['UsedBK', 'UsedCYM', 'PagesBK', 'PagesCYM', 'UsedBK_daily', 'UsedCYM_daily'],
                                       'average_val': ['PagesBK_daily',	'PagesCYM_daily', 'CostPerBK',
                                                       'CostPerCYM', 'PagesPerBK', 'PagesPerCYM']}

wjw_data_dic = [{'WJW': 'WJW4145', 'Serial_No': 'E79028J1N561471', 'Location': 'Fr. Frank', 'Contact': 'Frank Bahar'}, {'WJW': 'WJW4149', 'Serial_No': 'E79028J1N561476', 'Location': 'default', 'Contact': 'Zimmerschied Harald'}, {'WJW': 'WJW4147', 'Serial_No': 'E79028J1N561477', 'Location': 'default', 'Contact': 'Nnaji Christina'}, {'WJW': 'WJW4144', 'Serial_No': 'E79028J1N561454', 'Location': 'Besprechung', 'Contact': 'Schäfer Viktoria'}, {'WJW': 'WJW4148', 'Serial_No': 'E79028J1N561465', 'Location': 'BeSt Fr. Schoenstedt', 'Contact': 'Schoenstedt Anna'}, {'WJW': 'WJW4150', 'Serial_No': 'E701028J1N561453', 'Location': 'default', 'Contact': 'Beuth Indra Christina'}, {'WJW': 'WJW4146', 'Serial_No': 'E19028H1N561157', 'Location': 'Büro Frau Antl', 'Contact': 'Antl Pia'}, {'WJW': 'WJW3824', 'Serial_No': 'E78290D0N170303', 'Location': 'A3 ', 'Contact': ' Schlachtanalge '}, {'WJW': 'WJW3852', 'Serial_No': 'E79015J0N198441', 'Location': 'default', 'Contact': 'Zieglgänsberger Sabina'}, {'WJW': 'WJW3833', 'Serial_No': 'KMND48645', 'Location': 'Cafe Mechtild', 'Contact': 'Bühnert Nadine'}, {'WJW': 'WJW3826', 'Serial_No': 'E74555E8J891717', 'Location': 'GF Büro', 'Contact': 'aaaa_wjw_allgemain noname'}, {'WJW': 'WJW3822', 'Serial_No': 'RC60609776', 'Location': 'Verwaltung Fr. Issiz', 'Contact': 'Papageorgiou Zoi'}, {'WJW': 'WJW3801', 'Serial_No': 'TH03YBJ17T', 'Location': 'Büro Frau Antl', 'Contact': 'Backes Werner'}, {'WJW': 'WJW3681', 'Serial_No': 'KM3F3905', 'Location': 'Taskalfa3051ci', 'Contact': 'Elektro'}, {'WJW': 'WJW3609', 'Serial_No': '-', 'Location': 'Elektronik 1', 'Contact': 'aaaa_wjw_allgemain noname'}, {'WJW': 'WJW3611', 'Serial_No': 'g004086', 'Location': 'Elektronik 1', 'Contact': 'aaaa_wjw_allgemain noname'}, {'WJW': 'WJW3596', 'Serial_No': 'XLL8533468', 'Location': 'Büro Hr. Wölfinger, Hr. Grodek, Hr. Ströder, Hr. Sokoliss', 'Contact': 'aaaa_wjw_allgemain noname'}, {'WJW': 'WJW3601', 'Serial_No': 'E69498D3J408704', 'Location': 'A5 1. OG ', 'Contact': ' Maurer '}, {'WJW': 'WJW3561', 'Serial_No': 'E73941K5N798822', 'Location': 'A21 Erdgeschoss (Büro Fahrdienst)', 'Contact': 'aaaa_wjw_allgemain noname'}, {'WJW': 'WJW3557', 'Serial_No': '-', 'Location': 'Büro Verw.1 (A3 Gebäude Schlachtanlage 1OG)', 'Contact': 'Beil Renate'}, {'WJW': 'WJW3546', 'Serial_No': '--', 'Location': 'Gästehaus', 'Contact': 'aaaa_wjw_allgemain noname'}, {'WJW': 'WJW3539', 'Serial_No': 'E74552D6J442270', 'Location': 'Gästehaus', 'Contact': 'Engelberger Simon'}, {'WJW': 'WJW3536', 'Serial_No': 'E69507D3J409146', 'Location': 'Gästehaus', 'Contact': 'aaaa_wjw_allgemain noname'}, {'WJW': 'WJW3526', 'Serial_No': 'E74552J7J439390', 'Location': 'A4 EG ', 'Contact': ' Markthalle '}, {'WJW': 'WJW3519', 'Serial_No': '-', 'Location': 'Gästehaus', 'Contact': 'aaaa_wjw_allgemain noname'}, {'WJW': 'WJW3428', 'Serial_No': 'E74552J5J989713', 'Location': 'Büro', 'Contact': 'Kühnl Winfried'}, {'WJW': 'WJW3366', 'Serial_No': 'CRY12414', 'Location': 'Floristik', 'Contact': 'Barth Birgit'}, {'WJW': 'WJW3365', 'Serial_No': 'XLL6139518', 'Location': 'Floristik', 'Contact': 'Barth Birgit'}, {'WJW': 'WJW3427', 'Serial_No': 'MY596D429T0498', 'Location': 'Elektronik 1', 'Contact': 'aaaa_wjw_allgemain noname'}, {'WJW': 'WJW3432', 'Serial_No': 'Orgarent 21963', 'Location': 'BeSt Fr. Schoenstedt', 'Contact': 'Willius Michaela'}, {'WJW': 'WJW3431', 'Serial_No': 'E66518H0J548904', 'Location': 'BeSt Fr. Schoenstedt', 'Contact': 'Willius Michaela'}, {'WJW': 'WJW3418', 'Serial_No': 'E66518H0J548899', 'Location': 'BeST Fr.Zherebina ', 'Contact': 'Zieglgänsberger Sabina'}, {'WJW': 'WJW3414', 'Serial_No': 'XAX5339135', 'Location': 'Elektronik 1', 'Contact': 'aaaa_wjw_allgemain noname'}, {'WJW': 'WJW3415', 'Serial_No': 'Wurde abgebaut', 'Location': 'Elektronik 1', 'Contact': 'aaaa_wjw_allgemain noname'}, {'WJW': 'WJW3409', 'Serial_No': '178983966803', 'Location': 'Elektronik 1', 'Contact': 'aaaa_wjw_allgemain noname'}, {'WJW': 'WJW3408', 'Serial_No': 'E66518D9J404618', 'Location': 'Elektronik 1', 'Contact': 'aaaa_wjw_allgemain noname'}, {'WJW': 'WJW3367', 'Serial_No': 'Orgarent 22188', 'Location': 'Büro Frau Antl', 'Contact': 'Backes Werner'}, {'WJW': 'WJW3348', 'Serial_No': 'E66518F0J523457', 'Location': 'Elektronik 1', 'Contact': 'aaaa_wjw_allgemain noname'}, {'WJW': 'WJW3351', 'Serial_No': 'Q630616435', 'Location': 'Pädagogik Abt. Support', 'Contact': 'aaaa_wjw_allgemain noname'}, {'WJW': 'WJW3385', 'Serial_No': 'E69498M0J145493', 'Location': 'Metall Werkstatt Büro 1', 'Contact': 'Wieland Frank'}, {'WJW': 'WJW3329', 'Serial_No': 'KYL13399', 'Location': 'Elektronik 1', 'Contact': 'aaaa_wjw_allgemain noname'}, {'WJW': 'WJW3326', 'Serial_No': 'XLL6139264', 'Location': 'Elektronik 1', 'Contact': 'aaaa_wjw_allgemain noname'}, {'WJW': 'WJW3324', 'Serial_No': 'N', 'Location': 'MFC-9332 CDW', 'Contact': 'Schreiner 3'}, {'WJW': 'WJW3184', 'Serial_No': 'E74552K4J513105', 'Location': 'Büro', 'Contact': 'Krist Sascha'}, {'WJW': 'WJW3310', 'Serial_No': 'SG3936207K8J', 'Location': 'Büro Coaches', 'Contact': 'aaaa_wjw_allgemain noname'}, {'WJW': 'WJW3300', 'Serial_No': 'N', 'Location': 'EcosysFS4100DN', 'Contact': 'Büro Coaches'}, {'WJW': 'WJW3143', 'Serial_No': 'E65730K8N686750', 'Location': 'Büro Hr. Wölfinger, Hr. Grodek, Hr. Ströder, Hr. Sokoliss', 'Contact': 'aaaa_wjw_allgemain noname'}, {'WJW': 'WJW3139', 'Serial_No': 'Orgarent-21741', 'Location': 'Büro Metzgerei (A3 Gebäude Schlachtanlage 1OG)', 'Contact': 'aaaa_wjw_allgemain noname'}, {'WJW': 'WJW3019', 'Serial_No': 'E69498J1J225635', 'Location': 'BeSt Fr. Schulz', 'Contact': 'Schneider Silva'}]


run_interval = 5

if __name__ == '__main__':
    print(ROOT)