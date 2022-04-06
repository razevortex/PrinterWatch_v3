import bcrypt
from Packages.SubPkg.const.ConstantParameter import ROOT
import os.path
from pathlib import Path


def get_hashed_password(inuser, inpass):
    usereg = f'{ROOT}user/{inuser}.txt'
    hashed = bcrypt.hashpw(inpass, bcrypt.gensalt())
    with open(usereg, 'w') as reg:
        reg.writelines(hashed.decode())

def knownUser(inuser):
    usereg = Path(f'{ROOT}user/{inuser}.txt')
    if os.path.exists(usereg):
        pw = input('enter pw:')
        return verifyU(inuser, usereg, pw)
    else:
        return False

def verifyU(inuser, inpass):
    usereg = Path(f'{ROOT}user/{inuser}.txt')
    with open(usereg, 'r') as reg:
        hashed = reg.read()
    if bcrypt.checkpw(inpass.encode('utf-8'), hashed.encode()):
        return inuser
    else:
        return False

def repeat_pw(pw=False):
    while pw is not True:

        p = input('enter pw')
        if input('repeat') == p:
            pw = p
            return pw


if __name__ == '__main__':
    verified = False
    while verified is not True:
        user = input('u r ?')
        verified = knownUser(user)
        if verified is not False:
            break
        pw = repeat_pw()
        get_hashed_password(user, pw.encode('utf-8'))
    print(verified)