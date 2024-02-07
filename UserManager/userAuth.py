from json import dumps, loads
from os import path
from pathlib import Path
import qrcode
from qrcode.image.pil import PilImage
from PIL import Image
import io
import base64
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
        if self.status == 0:
            return False
        if kwargs.get('_pass', False):
            if hashlib.sha256(bytes(kwargs.get('_pass'), 'utf-8')).hexdigest() == self.__getattribute__('_pass'):
                self.status = 5
                kwargs.update({'token': None})
                return kwargs
            else:
                self.status -= 1
                return False
                
        if kwargs.get('auth2_key', False):
            if pyotp.TOTP(self.__getattribute__('auth2_key')).verify(kwargs.get('auth2_key')):
                self.status = 5
                return SessionObj().create_token(self.username)
            else:
                self.status -= 1
                return False
        return False
        
    def export(self):
        return {slot: self.__getattribute__(slot) for slot in self.__slots__}

    def __repr__(self):
        return ''.join([f'{slot}: {self.__getattribute__(slot)}' for slot in self.__slots__])
    
    @classmethod
    def create_new(cls, **kwargs):
        t_dict = {'status': 5, 'TTT': True, 'permission': 0, 'config': []}
        t_dict.update({key: val for key, val in kwargs.items() if key in ('username', '_pass', 'auth2_key')})
        return cls(**t_dict)
        
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

def qr_key_gen(username='', _pass='', **kwargs):
    _pass = hashlib.sha256(bytes(_pass, 'utf-8'))
    auth2_key = pyotp.random_base32()
    uri = pyotp.totp.TOTP(auth2_key).provisioning_uri(name=username, issuer_name='printerwatch')
    qr = qrcode.make(uri)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    return {'username': username, '_pass': _pass.hexdigest(), 'auth2_key': auth2_key, 'qr': base64.b64encode(buffer.getvalue()).decode()}
    

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

    def create_new(self, **kwargs):
        if kwargs.get('username', False):
            if self.user_exists(kwargs.get('username')) is False and len(kwargs.get('username')) >= 4:
                temp = qr_key_gen(**kwargs)
                print(temp)
                UserLib.name_index += [kwargs.get('username')]
                UserLib.obj += [UserObject.create_new(**temp)]
                self.save()
                return temp
        return {}
        
    #def create_user(self, name):
    #    if not self.user_exists(name) is False and len(name) >= 4:
    #        UserLib.name_index += [name]
    #        UserLib.obj += [UserObject.create_new_from_terminal(name)]
    #    print(UserLib.obj)
    #    self.save()

    def user_exists(self, name):
        if name in UserLib().name_index:
            return UserLib().name_index.index(name)
        return False

    def is_valid_user(self, name):
        obj = UserLib.obj[self.user_exists(name)]
        if obj:
            if obj.status != 0:
                return True
        return False

    def user_(self, **kwargs):
        print('user_ foo')
        if not self.user_exists(kwargs.get('username', '')) is False:
            if kwargs.get('token', False):
                temp = SessionObj().validate(**kwargs.get('token'))
                if temp:
                    return temp
            got = UserLib.obj[self.user_exists(kwargs.get('username', ''))].verify_creds(**kwargs)
            self.save()
            return got if got else {}
        return {}

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
