from pathlib import Path
import os
from Packages.StaticVar import *
import time
import pyotp
import qrcode

user_object_keys = ('username', '_pass', 'auth2_key', 'status', 'permission', 'config')
STATUS_DEFAULT = 5