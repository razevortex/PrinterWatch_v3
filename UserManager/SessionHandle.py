from printerwatch.UserManager.StaticVar import *
import hashlib
from json import dumps, loads
from os import path


class SessionObj(dict):
    file = Path(DB_DIR, 'session.json')

    def __init__(self, **kwargs):
        super().__init__(dict())
        self._load()

    def _load(self):
        if path.exists(SessionObj.file):
            with open(SessionObj.file, 'r') as f:
                self.update({obj.__name__: obj for obj in [TimeoutToken.load(key, val) for key, val in loads(f.read()).items()]})
        else:
            return {}

    def _save(self):
        json_obj = {key: val.export() for key, val in self.items() if not val.export() is None}
        with open(SessionObj.file, 'w') as f:
            return f.write(dumps(json_obj))

    def create_token(self, user):
        temp = TimeoutToken.create(user)
        self[temp.__name__] = temp
        self._save()
        return {'fields': [['hidden', 'timetoken', temp.__name__], ['hidden', 'username', user]]}

    def validate(self, **kwargs):
        token, user, valid = kwargs.get('timetoken', ''), kwargs.get('username', ''), False
        if self.get(token, False):
            valid = self[token].update_timestamp(user)
        self._save()
        return valid


class TimeoutToken(object):
    __name__ = ''

    def __init__(self, key, user, timestamp):
        self.__name__ = key
        self.username = user
        self.timestamp = timestamp

    @classmethod
    def load(cls, key, val):
        return cls(key, val[0], dt.strptime(val[1], TIMETOKEN_FORMAT))

    @classmethod
    def create(cls, user):
        timestamp = dt.now()
        timestring = timestamp.strftime(TIMETOKEN_FORMAT)
        return cls(hashlib.sha256(bytes(timestring, 'utf-8')).hexdigest(), user, timestamp)

    def update_timestamp(self, user):
        if self.in_time() and user == self.username:
            self.timestamp = dt.now()
            return {'fields': [['hidden', 'username', self.username],
                               ['hidden', 'timetoken', self.__name__]]}
        return False

    def in_time(self):
        if dt.now() - self.timestamp < TIMEOUT_DEFAULT:
            return True
        return False

    def export(self):
        if self.in_time():
            return [self.username, self.timestamp.strftime(TIMETOKEN_FORMAT)]
        else:
            return None

    def __repr__(self):
        return f'{self.__name__}: {self.username} > {self.timestamp}'


test = SessionObj()
#test.create_token('admin')
for key, val in test.items():
    print({'timetoken': key, 'username': val.username})
    print(test.validate(**{'timetoken': key, 'username': val.username}))
