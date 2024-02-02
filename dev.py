from printerwatch.DataManager.DataSet import DataBase
from printerwatch.PrinterRequest.main import RequestDummy as req
db = DataBase()

def print_libs():
    [print(f'{key}:\n{val}\n') for key, val in db.__dict__.items()]

def ip_req(ip):
    temp = req(ip)
    
