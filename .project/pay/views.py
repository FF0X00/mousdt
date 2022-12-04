from . import bp
from flask import request, redirect, url_for, render_template, jsonify, g, current_app
from utils.function import epay_sign
from utils import function
from utils import api
from utils import scheduler
from models import OrderModel, TransferModel
import config
import time
from utils.function import order_paid_amount, get_config, decrypt, encrypt
import re
from utils import restful
from exts import db, cache
from utils.api import is_API_work

@bp.route('/',methods=['GET','POST'])
def index():
    return ""


def order_submit_error(error_msg):
    return_data = {}
    return_data['code'] = -1
    return_data['msg'] = error_msg
    return jsonify(return_data)


@bp.route('/submit.php',methods=['GET','POST'])
def epay_order_submit():
    if request.method == 'POST':
        request_data = request.json
    elif request.method == 'GET':
        request_data = request.args
    else:
        return "request method err"

    # 简单HTML注入检查
    for temp in request_data:
        if "<" in request_data[temp] or ">" in request_data[temp]:
            return restful.params_err(message='input invalid')

        if re.search(r"(<\s+?img)|(<\s+?script)", request_data[temp]):
            return 'input invalid'

    order_submit_data = {}
    order_submit_data['pid'] = request_data.get('pid')
    order_submit_data['type'] = request_data.get('type')
    order_submit_data['out_trade_no'] = request_data.get('out_trade_no')
    order_submit_data['notify_url'] = request_data.get('notify_url')  # 支付成功后的回调通知地址
    order_submit_data['return_url'] = request_data.get('return_url')  # 支付成功后的跳转地址
    order_submit_data['name'] = request_data.get('name')
    order_submit_data['money'] = request_data.get('money')
    order_submit_data['sign'] = request_data.get('sign')
    order_submit_data['sign_type'] = request_data.get('sign_type')
    order_submit_data['sitename'] = request_data.get('sitename')
    order_submit_data['param'] = request_data.get('param')


    # 支付方式
    if order_submit_data['type'] == 'TRON':
        contract_type = 'TRON'
    else:
        contract_type = 'TRON'

    if order_submit_data['sign_type'] != "MD5":
        return order_submit_error('sign type err')

    try:
        int(order_submit_data['money'])
    except:
        return order_submit_error('only integer price')
    if request_data.get('pid') is None or request_data.get('type') is None or request_data.get('out_trade_no') is None \
            or request_data.get('notify_url') is None or request_data.get('notify_url') is None or request_data.get('return_url') is None \
            or request_data.get('name') is None or request_data.get('money') is None or request_data.get('sign') is None or request_data.get('sign_type') is None:
        return order_submit_error('para miss')

    # 签名校验
    sign_real = epay_sign(order_submit_data)

    if order_submit_data['sign'].lower() != sign_real.lower():
        return order_submit_error('sign fail')

    if not is_API_work(contract_type):
        return order_submit_error('API not work')


    # 创建订单
    order = OrderModel()
    order.notify_type = 'epay'
    order.contract_type = contract_type
    order.merchant_id = order_submit_data['pid']
    order.merchant_order_id = order_submit_data['out_trade_no']
    order.notify_url = order_submit_data['notify_url']
    order.return_url = order_submit_data['return_url']
    order.merchant_good_name = order_submit_data['name']
    order.price = order_submit_data['money']
    order.create_time = int(time.time())
    order.end_time = order.create_time + int(get_config('order_duration'))
    order = order.create()

    if not order:
        return order_submit_error('no free wallet')

    token = encrypt(str(order.id).encode(), get_config('encrypt_key')).decode()

    # 跳转支付页面
    return redirect(f"/page/pay/index.html?token={token}" )


@bp.route('/check_order', methods=['POST'])
def check_order():
    input_data = request.get_json()
    token = input_data.get('token')

    if token:
        try:
            order_id = int(decrypt(input_data['token'], get_config('encrypt_key')))
        except:
            return restful.params_err()
        order = OrderModel.query.filter( (OrderModel.id == order_id) ).first()

        if not order:
            return restful.params_err()

        if order.status == 1:
            return restful.ok(data={'status': 1, 'return_url': order.return_url})
        if order.status == -1:
            return restful.ok(data={'status': -1}, message='error')
        if order.status == 0:
            paid_transfer_list = TransferModel.query.filter(TransferModel.order_id == order.id).all()
            paid_transfer_list = [temp.to_dict() for temp in paid_transfer_list]


            return restful.ok(data={
                'status': 0,
                'order_price': order.price,
                'wallet_address': order.wallet_address,
                'contract_type': order.contract_type,
                'remain_time': order.end_time - int(time.time()),
                'transfer_items': paid_transfer_list
            })

    else:
        return restful.params_err()

@bp.route('/test/', methods=['GET', 'POST'])
def test():
    print(test1)

    return ""

