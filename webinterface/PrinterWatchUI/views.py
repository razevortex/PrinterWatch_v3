import sys
from json import dumps
from datetime import timedelta
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.http import HttpRequest
sys.path.insert(0, '/home/razevortex/PrinterWatch_v3')
from Packages.DataManager.DataSet import DataBase
from Packages.UserManager.userAuth import uLib



# Create your views here.

db = DataBase()

def mainpage(request):
    keys = ["display_name", "model", "ip", "cartridges"]
    keys, items = db.get_overview_table()
    return render(request, 'head.html', {'keys': keys, 'data': items})


def plot(request):
    if request.method == "POST":
        req = {key: val for key, val in request.POST.items()}
        if uLib.user_(**req):
            context = {'fields': [['hidden', key, val] for key, val in request.POST.items() if key in ('username', 'timetoken')]}
            data = dumps(db.generate_plot('Prints', search='ECO', timeframe=timedelta(days=28)))
            context.update({'data': data})
            return render(request, 'plot.html', context)
    return render(request, 'login.html', {'title': 'Login', 'href': '/', 'submit': 'Submit',
                                          'fields': [['text', 'username', ''], ['password', '_pass', '']]})


@csrf_protect
def login(request):
    if request.method == "POST":
        auth = {'username': request.POST.get('username', ''),
                '_pass': request.POST.get('_pass', ''),
                'fact2': request.POST.get('fact2')}
        context = uLib.user_(**auth)
        if context:
            return render(request, 'login.html', {key: val for key, val in context.items()})
    context = {'title': 'Login', 'href': '/', 'submit': 'Submit',
                'fields': [['text', 'username', ''], ['password', '_pass', '']]}
    #formtemp ='/', [['text', 'username', ''], ['password', '_pass', '']]
    return render(request, 'login.html', {'title': 'Login', 'href': '/', 'submit': 'Submit',
                'fields': [['text', 'username', ''], ['password', '_pass', '']]})


'''[print(f'{key}: {val}\n') for key, val in request.POST.items()]
        if request.POST.get('username', False):
            user = uLib.user_(request.POST.get('username'))
            print(user)
            if not user is None:
                for key in ('_pass', 'fact2'):
                    print(key)
                    if request.POST.get(key, False):

                        if user.verify_creds(key, request.POST.get(key)):
                            if key == '_pass':
                                print('true')
                                return render(request, 'login.html',
                                              {
                                                    'username': user.username,
                                                    'form': '/',
                                                    'inputs': [['password', 'fact2', ''], ['hidden', 'username', '']]})
                            if key == 'fact2':
                                print('true')
                                return render(request, 'login.html',
                                              {
                                                        'username': user.username,
                                                        'form': '/main/plot/',
                                                        'inputs': [['hidden', 'username', '']]})'''
