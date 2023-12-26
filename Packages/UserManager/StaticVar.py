from pathlib import Path
import os
from Packages.StaticVar import *
from datetime import timedelta, datetime as dt
import time
import pyotp
import qrcode

user_object_keys = ('username', '_pass', 'auth2_key', 'status', 'TTT', 'permission', 'config')
STATUS_DEFAULT = 5
TIMEOUT_DEFAULT = timedelta(minutes=15)
TIMETOKEN_FORMAT = '%d.%m.%Y %H:%M:%S'