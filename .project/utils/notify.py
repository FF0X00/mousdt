import requests
import config
from flask import current_app

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}


def epay_notify(order):
    notify_url = order.notify_url
    notify_data = {}
    notify_data['pid'] = order.merchant_id
    notify_data['trade_no'] = order.id
    notify_data['out_trade_no'] = order.merchant_order_id
    notify_data['type'] = order.currency
    notify_data['name'] = order.merchant_good_name
    notify_data['money'] = order.price
    notify_data['trade_status'] = "TRADE_SUCCESS"
    # notify_data['param'] = None
    notify_data['sign'] = None
    notify_data['sign_type'] = "MD5"
    from utils.function import epay_sign
    sign_real = epay_sign(notify_data)

    notify_data['sign'] = sign_real
    current_app.logger.debug(f"发送回调: url:{notify_url}, data:{notify_data}")


    try:
        requests.get(notify_url, params=notify_data, headers=headers)
    except:
        if "https" in notify_url:
            notify_url = notify_url.replace("https", "http")
            requests.get(notify_url, params=notify_data, headers=headers)