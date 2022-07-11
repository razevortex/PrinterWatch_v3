from django.shortcuts import render
from django.http import HttpResponse
from Packages.SubPkg.foos import *
from Packages.userIN import *


# Create your views here.
def mainframeset(request, safe=True):
    run_background_requests(7)
    if safe:
        user = False
        if user is not True:
            if request.method == 'POST':
                loginput = request.POST
                _user = loginput.get('user')
                _pass = loginput.get('pass')
                user = verifyU(_user, _pass)
                user, sudo = decrypt_user(encrypt_user(user))
            if user is not False:
                color, time = timestamp_from_com()
                if sudo:
                    return render(request, 'mainframeset.html', {'cc': color, 'ts': time, 'Ur': encrypt_user(user)}) #user_token_switch(user)})
                else:
                    return render(request, 'mainframeset_non_sudo.html',
                                  {'cc': color, 'ts': time, 'Ur': encrypt_user(user)})  # user_token_switch(user)})
            else:
                return render(request, 'login.html')
    else:
        color, time = timestamp_from_com()
        return render(request, 'mainframeset.html', {'cc': color, 'ts': time})


def help(request):
    return render(request, 'help.html', {})


def signup(request):
    err = ('If you enter your desired user information here and some of the admins canactivate it then.', 'white')
    if request.method == 'POST':
        loginput = request.POST
        _user = loginput.get('user')
        _pass = loginput.get('pass')
        _repeat = loginput.get('repeat')
        name_avaible, err_code = username_is_avaible(_user)
        if name_avaible:
            pass_valid, err_code = password_met_requirements(_pass, _repeat)
            if pass_valid:
                err = (err_code, 'green')
                add_reg_user(_user, _pass)
                return render(request, 'signin.html', {'msg': err[0], 'color': err[1]})
            else:
                err = (err_code, 'red')
                return render(request, 'signin.html', {'msg': err[0], 'color': err[1]})

        else:
            err = (err_code, 'red')
            return render(request, 'signin.html', {'msg': err[0], 'color': err[1]})

    return render(request, 'signin.html', {'msg': err[0], 'color': err[1]})

