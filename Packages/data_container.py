from Packages.SubPkg.foos import *
from Packages.SubPkg.foos import *

key_list = ['Serial_No', 'IP', 'Manufacture', 'Model', 'Contact', 'Location', 'Note', 'Toner_Models', 'Toner_Prices']

class Data_Container(object):
    def __init__(self):
        self.key_list = {'head_keys': [], 'data_keys': header['request_db']}
        self.db_filtered = []
        cli = dbClient()
        cli.updateData()
        spec = dbClientSpecs()
        overWrite = LibOverride()
        temp = []
        head = {}
        for client in cli.ClientData:
            req = dbRequest(client['Serial_No'])
            req.updateData()
            data = req.ClientData
            for client_spec in spec.ClientData:
                if client_spec['Serial_No'] == client['Serial_No']:
                    client.update(client_spec)
            for client_ow in overWrite.ClientData:
                if client_ow['ID'] == client['Serial_No']:
                    for key, val in client_ow.items():
                        if key != 'ID':
                            if val != 'NaN':
                                client[key] = val
            head = client
            temp.append((head, data))
        self.key_list['head_keys'] = list(head.keys())
        self.db_collection = temp


    def filter_db_collection(self, keyword):
        temp = []
        for db_client in self.db_collection:
            head, data = db_client
            if keyword != '':
                if keyword in list(head.values()):
                    head_vals = []
                    data_vals = []
                    for key in self.key_list['head_keys']:
                        head_vals.append(head[key])
                    for line in data:
                        t_line = []
                        for key in self.key_list['data_keys']:
                            t_line.append(line[key])
                        data_vals.append(t_line)
                    temp.append((head_vals, data_vals))

            else:
                head_vals = []
                data_vals = []
                for key in self.key_list['head_keys']:
                    head_vals.append(head[key])
                for line in data:
                    t_line = []
                    for key in self.key_list['data_keys']:
                        t_line.append(line[key])
                    data_vals.append(t_line)
                print(head_vals)
                temp.append((head_vals, data_vals))
            self.db_filtered.append(temp)

    def give_html_table_lists(self, keyword=''):
        self.filter_db_collection(keyword)
        table_data = list(self.key_list['head_keys'])
        for i in self.db_filtered:
            if len(i) == 2:
                head, data = i
                table_data.append(head)

        return table_data

if __name__ == '__main__':
    cont = Data_Container()
    cont.give_html_table_lists()