from json import dumps, loads
from os import path
from pathlib import Path
from PIL import Image
import hashlib
from printerwatch.UserManager.StaticVar import *
from printerwatch.UserManager.SessionHandle import SessionObj
from printerwatch.GlobalClasses import LockedSlots


class UserObject(LockedSlots):
    __slots__ = user_object_keys

    def __init__(self, **kwargs):
        [self.__setattr__(key, val) for key, val in kwargs.items()]
        super().__init__(*user_object_keys[:3])

    def verify_creds(self, **kwargs):
        if self.status != 0:
            for key, val in kwargs.items():
                if key == '_pass' and val != '':
                    if hashlib.sha256(bytes(val, 'utf-8')).hexdigest() == self.__getattribute__('_pass'):
                        self.status = 5
                        return {'title': '2 Fact Auth', 'href': '/', 'submit': 'Submit',
                                'fields': [['hidden', 'username', self.username], ['text', 'fact2', '']]}
                    else:
                        self.status -= 1
                        return False
                if key == 'fact2' and val != '':
                    if pyotp.TOTP(self.__getattribute__('auth2_key')).verify(val):
                        self.status = 5
                        token = SessionObj().create_token(self.username)
                        token.update({'title': f'Hi {self.username},', 'href': '/main/plot/', 'submit': 'Enter'})
                        #        'fields': [['hidden', 'username', self.username],
                        #                   ['hidden', 'timetoken', token['timetoken']]]}
                        return token
                    else:
                        self.status -= 1
                        return False
        return None

    '''def cred(self):
        if self.status:
            entered = hashlib.sha256(bytes(input('enter password:'), 'utf-8'))
            #print(hash(entered), self.__getattribute__('pass'))
            if self.__getattribute__('_pass') == entered.hexdigest():
                if pyotp.TOTP(self.__getattribute__('auth2_key')).verify(input('enter 2 auth:')):
                    return True
        return False'''

    def export(self):
        return {slot: self.__getattribute__(slot) for slot in self.__slots__}

    def __repr__(self):
        return ''.join([f'{slot}: {self.__getattribute__(slot)}' for slot in self.__slots__])

    @classmethod
    def create_new_from_terminal(cls, name):
        password = False
        while not password:
            raw = input(f'{name} create your password:')
            if len(raw) >= 4:
                password = hashlib.sha256(bytes(raw, 'utf-8')) if input(f'{name} verify password:') == raw else False

        print('creating key for 2 Fact Auth make sure to store and setup it properly')
        factAuth = pyotp.random_base32()
        uri = pyotp.totp.TOTP(factAuth).provisioning_uri(name=name, issuer_name='system')
        qr = qrcode.make(uri)
        qr._img.show()
        input("Enter to End")
        print(', '.join([f'{key}: {val}' for key, val in {'username': name, '_pass': password.hexdigest(), 'auth2_key': factAuth, 'status': 5, 'TTT': True, 'permission': 0, 'config': []}.items()])) 
        return cls(**{'username': name, '_pass': password.hexdigest(), 'auth2_key': factAuth, 'status': 5, 'TTT': True, 'permission': 0, 'config': []})


class UserLib(object):
    obj = []
    name_index = []
    file = Path(DB_DIR, 'user.json')

    def __init__(self):
        self.load()

    def save(self):
        temp = self._import()
        try:
            with open(UserLib.file, 'w') as f:
                f.write(dumps(self._export()))
        except:
            print('An Error Occured file wasnt saved')
            with open(UserLib.file, 'w') as f:
                f.write(dumps(temp))

    def create_user(self, name):
        if not self.user_exists(name) is False and len(name) >= 4:
            UserLib.name_index += [name]
            UserLib.obj += [UserObject.create_new_from_terminal(name)]
        print(UserLib.obj)
        self.save()

    def user_exists(self, name):
        if name in UserLib.name_index:
            return UserLib.name_index.index(name)
        return False

    def is_valid_user(self, name):
        obj = UserLib.obj[self.user_exists(name)]
        if obj:
            if obj.status != 0:
                return True
        return False

    def user_(self, **kwargs):
        if not self.user_exists(kwargs.get('username', '')) is False:
            if 'timetoken' in kwargs.keys():
                return SessionObj().validate(**kwargs)
            got = UserLib.obj[self.user_exists(kwargs.get('username', ''))].verify_creds(**kwargs)
            self.save()
            return got

    def auth_user(self, name):
        if name in UserLib.name_index:
            if UserLib.obj[UserLib.name_index.index(name)].cred():
                print('Worked')
                return UserLib.obj[UserLib.name_index.index(name)].cred()

    def _export(self):
        return [obj.export() for obj in UserLib.obj]

    def _import(self):
        with open(UserLib.file, 'r') as f:
            return loads(f.read())

    def load(self):
        if path.exists(UserLib.file):
            for obj in self._import():
                if obj['username'] not in UserLib.name_index:
                    UserLib.obj += [UserObject(**obj)]
            UserLib.name_index += [obj.username for obj in UserLib.obj]
        else:
            with open(UserLib.file, 'w') as f:
                f.write(dumps([]))


uLib = UserLib()
#uLib.auth_user('admin')
