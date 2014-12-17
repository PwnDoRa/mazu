# -*- coding: utf-8 -*-
""" Inserting an user and an authkey

    ./manage.py shell
    >>> from django.contrib.auth.models import User
    >>> from authkey.models import AuthKey
    >>> User.objects.create_user('username', 'username@example.com', 'password').save()
    >>> usr = User.objects.get(username='username')
    >>> AuthKey(owner=usr, ident='ident', secret='secret', pubchans='["chan1"]', subchans='["chan1"]').save()
"""

import json
import config
import sys
import os

# Django configurations
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(PROJECT_ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.production")

from django.contrib.auth.models import User
from utils import custom_split
from brokers.models import Log
from brokers.models import ConnStats
from brokers.models import AuthKey


class Database(object):
    def __init__(self):
        pass

    def log(self, row):
        enc = json.dumps(row)
        Log(data=enc).save()


    def connstats(self, ak, uid, stats):
        res = None
        try:
            res = ConnStats.objects.get(ak=ak)
        except:
            import traceback
            traceback.print_exc()

        if not res:
            enc = json.dumps(stats)
            uid = User.objects.get(username=uid)
            ConnStats(ak=ak, uid=uid, data=enc).save()
        else:
            rid = res.uid
            data = res.data
            dec = json.loads(data)
            new = dict([(k, stats[k]+dec.get(k, 0)) for k in stats])
            enc = json.dumps(new)
            res.data = enc
            res.uid = rid
            res.save()

    def get_authkey(self, ident):
        res = None
        try:
            res = AuthKey.objects.get(ident=ident)
        except:
            import traceback
            traceback.print_exc()

        if not res: return None

        pubchans = custom_split(res.pubchans)
        subchans = custom_split(res.subchans)

        return dict(secret=res.secret, ident=res.ident, pubchans=pubchans,
            subchans=subchans, owner=res.owner
        )