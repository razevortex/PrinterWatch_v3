import codecs
import os.path
from os import listdir
from pathlib import Path

import bcrypt

from Packages.SubPkg.const.ConstantParameter import ROOT
from Packages.SubPkg.csv_handles import userDB


class StrHexCrypt(object):
    def __init__(self, text: str, salt: int, revert=False):
        self.userDB = get_user_db(total=True)
        self.user = [f.replace('.txt', '') for f in listdir(f'{ROOT}user/') if 'Config' not in f]
        with open(f'{ROOT}user/_sudo.txt') as admins:
            self.admin = [admin.strip() for admin in admins.readlines()]
        self.salt = salt
        self.text = text
        if revert:
            self.text = self.decrypting()
        else:
            self.text = self.encrypting()

    def decrypting(self):
        temp = self.split_n_fuse(self.text)
        for _ in range(1, self.salt):
            x = self.salt - _
            temp[0] = str(hex((int(temp[0], base=16) ^ x) % 254))[2:]
            if len(temp[0]) == 1:
                temp[0] = '0' + temp[0]
            temp = self.shift_pos(temp, shift_range=_+1, pos=0, vector='left')
            temp = self.shift_pos(temp, shift_range=_+1, pos=1, vector='right')
        return self.plain_to_hex(self.invert_pos(temp), reverse=True)

    def encrypting(self):
        temp = self.invert_pos(self.plain_to_hex(self.text))
        for _ in range(1, self.salt):
            temp = self.shift_pos(temp, shift_range=_+1, pos=1, vector='left')
            temp = self.shift_pos(temp, shift_range=_+1, pos=0, vector='right')
            x = _
            temp[0] = str(hex((int(temp[0], base=16) ^ x) % 254))[2:]
            if len(temp[0]) == 1:
                temp[0] = '0' + temp[0]
        return self.split_n_fuse(temp)

    def plain_to_hex(self, get, reverse=False):
        if reverse:
            temp = self.split_n_fuse(get)
            binary_str = codecs.decode(temp, "hex")
            return str(binary_str, 'utf-8')
        else:
            temp = ''
            for letter in get.encode():
                t = hex(letter)
                temp += str(t)[2:]
            return self.split_n_fuse(temp)

    def split_n_fuse(self, input):
        if type(input) == str:
            t = []
            for i in range(0, len(input) // 2):
                x = i * 2
                t.append(input[x:x + 2])
            return t
        elif type(input) == list:
            t = ''
            for i in input:
                t += i
            return t

    def shift_pos(self, hex_arr, shift_range=1, pos=0, vector='right'):
        for _ in range(0, shift_range):
            crypted_arr = []
            if vector == 'right':
                hold = hex_arr[-1][pos]
                for hex in hex_arr:
                    string = ''
                    for i in range(len(hex)):
                        if i != pos:
                            string += hex[i]
                        else:
                            string += hold
                            hold = hex[i]
                    crypted_arr.append(string)
            elif vector == 'left':
                hold = hex_arr[0][pos]
                for hex in hex_arr[::-1]:
                    string = ''
                    for i in range(len(hex)):
                        if i != pos:
                            string += hex[i]
                        else:
                            string += hold
                            hold = hex[i]
                    crypted_arr.append(string)
            return crypted_arr

    def invert_pos(self, hex_arr):
        return hex_arr[::-1]

    def validate(self):
        print(self.user, self.admin)
        user = False
        admin = False
        for line in self.userDB:
            if self.text in line['User']:
                user_dict = line
                if line['State'] != 'applied':
                    user = line['User']
                if line['State'] == 'sudo':
                    admin = True
        return user, admin
        '''print(self.user, self.admin)
        if self.text in self.user:
            user = self.text
        else:
            user = False
        if user in self.admin:
            return user, True
        else:
            return user, False
        '''

    def cypher(self):
        hex = self.text
        return hex


def decrypt_user(input):
    cryptor = StrHexCrypt(input, 23, revert=True)
    print(cryptor.text)
    return cryptor.validate()


def encrypt_user(input):
    cryptor = StrHexCrypt(input, 23)
    return cryptor.cypher()


def user_token_switch(input, shorten_token=True, got_user=True):
    t_arr = []
    for user in [f for f in listdir(f'{ROOT}user/') if 'Config' not in f]:
        with open(f'{ROOT}user/{user}', 'r') as txt:
            auth_token = txt.read()
            if shorten_token:
                t_arr.append((auth_token[7:14], user.replace('.txt', '')))
            else:
                t_arr.append((auth_token, user.replace('.txt', '')))
    for set in t_arr:
        if set[0] == input and not got_user:
            return set[1]
        if set[1] == input and got_user:
            return set[0]
    return False


def username_is_avaible(new_user):
    if len(new_user) < 4:
        return False, 'username needs at least 4 characters'
    for user in [f for f in listdir(f'{ROOT}user/') if 'Config' not in f]:
        if new_user == user:
            return False, 'username already is taken'
    with open(f'{ROOT}user/_add.txt', 'r') as pending:
        for pending_user in pending.readlines():
            if new_user in pending_user:
                return False, 'username register ask admin to verify request'
    if ' ' in new_user:
        return False, 'username must not contain "SPACE" characters'
    return True, new_user


def password_met_requirements(pass_, _pass):
    if 4 > len(str(pass_)) or len(str(pass_)) > 16:
        return False, f'password length {len(pass_)} did not fit in 4-16 characters'
    if pass_ != _pass:
        return False, 'repeated password did not match the original'
    return True, 'succesful registered waiting for verification by admin'

def add_reg_user(user, _pass):
    hashed_pw = bcrypt.hashpw(_pass.encode('utf-8'), bcrypt.gensalt()).decode()
    string = user + ' ' + hashed_pw + '\n'
    with open(f'{ROOT}user/_add.txt', 'r') as pending:
        t_arr = [pending_user for pending_user in pending.readlines()]
    t_arr.append(string)
    with open(f'{ROOT}user/_add.txt', 'w') as pending:
        pending.writelines(t_arr)


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


def AuTo(uToken):
    try:
        inuser, inpass = uToken
        usereg = Path(f'{ROOT}user/{inuser}.txt')
        with open(usereg, 'r') as reg:
            hashed = reg.read()
        if bcrypt.checkpw(inpass.encode('utf-8'), hashed.encode()):
            return True
        else:
            return False
    except:
        return False


def AuToView(req):
    if req.method == 'POST':
        loginput = req.POST
        _user = loginput.get('user')
        _pass = loginput.get('pass')
        if AuTo((_user, _pass)):
            return _user, _pass
    else:
        return False


def repeat_pw(pw=False):
    while pw is not True:
        p = input('enter pw')
        if input('repeat') == p:
            pw = p
            return pw


def get_user_db(total=False):
    db = userDB()
    t_dic = {}
    if not total:
        for line in db.ClientData:
            t_dic[line['User']] = line['State']
        return t_dic
    else:
        return list(db.ClientData)

if __name__ == '__main__':
    print(get_user_db())
    #print(str(bcrypt.hashpw(''.encode('utf-8'), bcrypt.gensalt())))
