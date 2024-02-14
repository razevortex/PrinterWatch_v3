#from printerwatch.PrinterObject.main import cLib, mLib, pLib

model_oid = (('ECOSYS M6635cidn', 'ECOSYS M3655idn', 'MFC-9142CDN', 'MFC-L3770CDW', 'MFC-L3750CDW',
               'TASKalfa 3051ci', 'TASKalfa 5052ci', 'TASKalfa 4002i', 'MFC-9332CDW', 'MFC-L8650CDW',
               'DCP-L3510CDW', 'MFC-9460CDN'),
              ('MFC-9142CDN', 'MFC-L3750CDW', 'MFC-L3770CDW', 'MFC-L8650CDW', 'MFC-9342CDW'))

model_dict = ({'location': '1.3.6.1.2.1.1.6.0'},
              {'contact': '1.3.6.1.2.1.1.4.0'})

VALID_OID = '1.3.6.1.2.1.1.1.0'

VALID_CLIENT_OID = {'KYOCERA': {'manufacturer': 'Kyocera',
                                'model': '1.3.6.1.2.1.43.5.1.1.16.1',
                                'serial_no': '1.3.6.1.2.1.43.5.1.1.17.1'},
                    'Brother': {'manufacturer': 'Brother',
                                'model': '1.3.6.1.2.1.25.3.2.1.3.1',
                                'serial_no': '1.3.6.1.2.1.43.5.1.1.17.1'}}

# toner are 2 values the first are the max value the second the current fill value
kyocera_toner_bw = {'Toner':({'B': '1.3.6.1.2.1.43.11.1.1.8.1.1'}, {'B': '1.3.6.1.2.1.43.11.1.1.9.1.1'})}

kyocera_toner_color = {'Toner':({'C': '1.3.6.1.2.1.43.11.1.1.8.1.1', 'M': '1.3.6.1.2.1.43.11.1.1.8.1.2',
                        'Y': '1.3.6.1.2.1.43.11.1.1.8.1.3', 'B': '1.3.6.1.2.1.43.11.1.1.8.1.4'},
                       {'C': '1.3.6.1.2.1.43.11.1.1.9.1.1', 'M': '1.3.6.1.2.1.43.11.1.1.9.1.2',
                        'Y': '1.3.6.1.2.1.43.11.1.1.9.1.3', 'B': '1.3.6.1.2.1.43.11.1.1.9.1.4'})}

kyocera_pages = {'Prints': '1.3.6.1.4.1.1347.42.3.1.1.1.1.1',
                 'Copies': '1.3.6.1.4.1.1347.42.3.1.1.1.1.2'}

taskalfa_pages = {'Prints': '1.3.6.1.4.1.1347.42.3.1.2.1.1.1.1',
                  'ColorPrints': '1.3.6.1.4.1.1347.42.3.1.2.1.1.1.3',
                  'Copies': '1.3.6.1.4.1.1347.42.3.1.2.1.1.2.1',
                  'ColorCopies': '1.3.6.1.4.1.1347.42.3.1.2.1.1.2.3'}

ecosys_pages = {'Prints': '1.3.6.1.4.1.1347.42.3.1.2.1.1.1.1',
                'ColorPrints': '1.3.6.1.4.1.1347.42.3.1.2.1.1.1.2',
                'Copies': '1.3.6.1.4.1.1347.42.3.1.2.1.1.2.1',
                'ColorCopies': '1.3.6.1.4.1.1347.42.3.1.2.1.1.2.2'}

brother_replacements = {'Default': ['<', '>', '=', '%', '(', ')',
                                    'class', '"items"', '"unit"', '"subhead"',
                                    'dt', 'dd', 'dl', 'span', 'Pages', '/List', 'pages',
                                    ' ', '.00', 'Cyan', 'Magenta', 'Yellow', 'Black'
                                    ],
                        'MFC-9460CDN': ['<', '>', '=', '%', '(', ')', 'CLASS', r'\n', 'TR', 'TD', 'NOWRAP',
                                        'TABLE', 'COL',
                                        'SPACING', 'BORDER', 'DT', 'DD', 'DD', 'SPAN', 'Pages', 'ALIGN',
                                        'pages', 'Doner',
                                        r'&nbsp;', ' ', '.00', 'Cyan', 'Magenta', 'Yellow', 'Black',
                                        '&nbsp;']
                        }

brother_urls = {'default': ('/general/status.html', '/general/information.html?kind=item'),
                'MFC-9460CDN': ('/main/main.html', '/etc/mnt_info.html?kind=item')}
# Execution Sandbox
if __name__ == '__main__':
	pass