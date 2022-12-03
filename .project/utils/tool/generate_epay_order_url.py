import requests
import json
import random
import collections
import urllib.parse
import hashlib
import config
from flask import current_app
from utils.function import get_config


def generate_epay_order_url():
    data = {}
    data['pid'] = 1
    data['type'] = 'USDT'
    data['notify_url'] = 'notify_url'
    data['return_url'] = 'return_url'
    data['out_trade_no'] = int(random.random()*10e10)
    data['name'] = 'test'
    data['money'] = 1
    data['sitename'] = ''
    data = dict(collections.OrderedDict(sorted(data.items())))

    sign = ''

    for i in data:
        if data[i] == '' or i == 'sign':
            continue
        if sign != '':
            sign += '&'


        sign += f"{i}={data[i]}"
    epay_merchant_key = get_config('epay_merchant_key')
    # epay_merchant_key = "diitapzgbrbbyfis"
    sign = hashlib.md5((sign + epay_merchant_key).encode('utf-8')).hexdigest()
    data['sign'] = sign
    data['sign_type'] = 'MD5'

    return "/api/pay/submit.php?" + "&".join([f"{temp}=" + urllib.parse.quote(str(data[temp]), safe="") for temp in data if data[temp] ])


#
# from create_app import create_app
#
# context_app = create_app()
# with context_app.app_context():
#     print(generate_epay_order_url())


