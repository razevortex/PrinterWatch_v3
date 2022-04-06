from django.shortcuts import render
from django.http import HttpResponse
from Packages.SubPkg.foos import *
from Packages.userIN import *
# Create your views here.


def mainframeset(request, safe=True):
    if safe:
        user = False
        if user is not True:
            if request.method == 'POST':
                loginput = request.POST
                _user = loginput.get('user')
                _pass = loginput.get('pass')
                user = verifyU(_user, _pass)
            if user is not False:
                color, time = timestamp_from_com()
                return render(request, 'mainframeset.html', {'cc': color, 'ts': time, 'Ur': user})
            else:
                return render(request, 'login.html')
    else:
        color, time = timestamp_from_com()
        return render(request, 'mainframeset.html', {'cc': color, 'ts': time})
