import os.path
from . import bp
from flask import request, make_response, redirect, url_for, render_template, jsonify, session
from utils.function import get_config, refresh_wallet
from werkzeug.security import check_password_hash
import json
from utils import restful
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from models import OrderModel, TransferModel, WalletModel, AdminModel, ConfigModel
import time
import datetime
import sqlalchemy
from exts import db, limiter
from utils.tool.generate_wallet import generate_wallet
from utils.api import get_TRON_transfer_list
from file_read_backwards import FileReadBackwards
from utils.tool.generate_epay_order_url import generate_epay_order_url
from utils.tool.QR_code import generate_QR_code
from utils.api import is_API_work, get_tron_balance


@bp.route("/login", methods=['POST'])
@limiter.limit("5/minute", override_defaults=True)
def login():
    request_data = json.loads(request.data)
    input_admin_username = request_data['username']
    input_admin_password = request_data['password']

    login_admin = AdminModel.query.filter(AdminModel.username == input_admin_username).first()
    if not login_admin:
        return restful.params_err()

    is_password_correct = check_password_hash(login_admin.password, input_admin_password)
    if not is_password_correct:
        return restful.params_err()

    # 生成管理员token
    token = create_access_token(identity='admin_' + str(login_admin.id))
    return_data = {}

    return_data['token'] = token
    return restful.ok(data=return_data)


@bp.route("/info", methods=['POST'])
def info():
    return_data = {"roles": ["admin"],
                   "introduction": "I am a super administrator",
                   "avatar": "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif",
                   "name": "Super Admin"}
    return restful.ok(data=return_data)


@bp.route("/logout", methods=['POST'])
def logout():
    return_data = "success"
    return restful.ok(data=return_data)


@bp.route("/dashboard", methods=['POST'])
def dashboard():
    input_data = request.get_json()
    return_data = {}
    # total_price_query = sqlalchemy.func.sum(OrderModel.price).label("total_price")
    # total_count_query = sqlalchemy.func.sum(sqlalchemy.sql.expression.case(value=OrderModel.status, whens={-1: 1}, else_=0)).label("total_count")
    # paid_count_query = sqlalchemy.func.sum(sqlalchemy.sql.expression.case(value=OrderModel.status, whens={1: 1}, else_=0)).label("paid_count")
    # record_query = db.session.query(
    #     total_price_query,
    #     total_count_query,
    #     paid_count_query
    # )

    record_query = OrderModel.query
    start_time = input_data.get("start_time")
    end_time = input_data.get("end_time")

    start_timestamp = int(time.mktime((datetime.datetime.now().replace(hour=0, minute=0, second=0,
                                                                       microsecond=0) - datetime.timedelta(
        days=7)).timetuple()))
    end_timestamp = int(time.mktime((datetime.datetime.now().replace(hour=0, minute=0, second=0,
                                                                     microsecond=0) + datetime.timedelta(
        days=1)).timetuple()))

    if start_time and end_time:
        start_timestamp_temp = int(datetime.datetime.strptime(start_time, "%Y-%m-%d").timestamp())
        end_timestamp_temp = int(datetime.datetime.strptime(end_time, "%Y-%m-%d").timestamp()) + 60 * 60 * 24
        # 开始大于结束的，大于等于180天的
        if start_timestamp_temp < end_timestamp_temp or end_timestamp_temp - start_timestamp_temp >= 60 * 60 * 24 * 180:
            start_timestamp = start_timestamp_temp
            end_timestamp = end_timestamp_temp

    record_result = record_query.filter(
        (OrderModel.create_time >= start_timestamp) & (OrderModel.create_time < end_timestamp)).all()

    return_data['income'] = sum([temp.price for temp in record_result if temp.status == 1])
    return_data['count'] = len(record_result)
    return_data['paid_count'] = len([temp for temp in record_result if temp.status == 1])

    echart_data_temp = []
    start_datetime = datetime.datetime.fromtimestamp(start_timestamp)
    end_datetime = datetime.datetime.fromtimestamp(end_timestamp)
    start_datetime_temp = start_datetime
    while True:
        end_datetime_temp = start_datetime_temp + datetime.timedelta(days=1)

        data = {}
        data['start_timestamp'] = int(start_datetime_temp.timestamp())
        data['end_timestamp'] = int(end_datetime_temp.timestamp())

        order_list = []
        for order in record_result:
            if data['start_timestamp'] <= order.create_time < data['end_timestamp']:
                order_list.append(order)

        data['income'] = sum([temp.price for temp in order_list if temp.status == 1])
        data['count'] = len(order_list)
        data['paid_count'] = len([temp for temp in order_list if temp.status == 1])

        # data['count'] = len(order_list)
        # order_list = [temp for temp in order_list if temp.paid_price > 0]
        # data['income'] = sum([temp.paid_price for temp in order_list])
        # data['paid_count'] = len([temp for temp in order_list])
        echart_data_temp.append(data)

        start_datetime_temp = end_datetime_temp
        if end_datetime_temp >= end_datetime:
            break

    echart_data = {}
    echart_data['x_axis_data'] = [datetime.datetime.fromtimestamp(temp['start_timestamp']).strftime('%m-%d') for temp in
                                  echart_data_temp]
    echart_data['paid_order_count_data'] = [temp['paid_count'] for temp in echart_data_temp]
    echart_data['income_data'] = [temp['income'] for temp in echart_data_temp]

    return_data['echart_data'] = echart_data
    return restful.ok(data=return_data)


@bp.route("/order", methods=['POST'])
def order():
    input_data = request.get_json()
    record_query = OrderModel.query
    sort = input_data.get("sort")
    limit = input_data.get("limit")
    current_page = input_data.get("page")
    start_time = input_data.get("start_time")
    end_time = input_data.get("end_time")
    merchant_id = input_data.get("merchant_id")

    if sort:
        if sort == 'desc':
            record_query = record_query.order_by(OrderModel.id.desc())
        else:
            record_query = record_query.order_by(OrderModel.id.asc())
    else:
        record_query = record_query.order_by(OrderModel.id.asc())

    if limit and int(limit) > 0 and int(limit) <= 100:
        per_page = int(limit)
    else:
        per_page = 20

    if start_time:
        start_timestamp = int(datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S").timestamp())
        record_query = record_query.filter(OrderModel.create_time >= start_timestamp)
    if end_time:
        end_timestamp = int(datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S").timestamp())
        record_query = record_query.filter(OrderModel.create_time <= end_timestamp)

    if merchant_id:
        record_query = record_query.filter(OrderModel.merchant_id == merchant_id)

    record_query = record_query.paginate(page=current_page, per_page=per_page, error_out=False)

    return_data = {}
    return_data['total'] = record_query.total
    return_data['items'] = [temp.to_dict() for temp in record_query.items]

    return restful.ok(data=return_data)


@bp.route("/order_detail", methods=['POST'])
def order_detail():
    order_id = request.get_json().get('id')
    order = OrderModel.query.filter(OrderModel.id == order_id).first()
    return_data = order.to_dict()
    return restful.ok(data=return_data)


@bp.route("/wallet_detail", methods=['POST'])
def wallet_detail():
    wallet_id = request.get_json().get('id')
    wallet = OrderModel.query.filter(WalletModel.id == wallet_id).first()
    return_data = wallet.to_dict()
    return restful.ok(data=return_data)


@bp.route("/wallet_refresh", methods=['POST'])
def wallet_refresh():
    input_data = request.get_json()

    force_refresh = True if input_data.get('force_refresh') else False
    refresh_wallet_id = input_data.get('id')

    if refresh_wallet_id:
        wallet = WalletModel.query.filter(WalletModel.id == refresh_wallet_id).first()
        refresh_wallet(wallet, force_refresh=True)
    else:
        wallet_list = WalletModel.query.filter(WalletModel.balance != 0).all()
        for wallet in wallet_list:
            refresh_wallet(wallet, force_refresh=force_refresh)

    return restful.ok()


@bp.route("/transfer_detail", methods=['POST'])
def transfer_detail():
    transfer_id = request.get_json().get('id')
    transfer = OrderModel.query.filter(WalletModel.id == transfer_id).first()
    return_data = transfer.to_dict()
    return restful.ok(data=return_data)


@bp.route("/order_notify", methods=['POST'])
def order_notify():
    order_id = request.get_json().get('id')
    order = OrderModel.query.filter(OrderModel.id == order_id).first()
    if order:
        order.notify()
    return restful.ok(data='ok')


@bp.route("/transfer", methods=['POST'])
def transfer():
    input_data = request.get_json()
    record_query = TransferModel.query
    limit = input_data.get("limit")
    current_page = input_data.get("page")
    start_time = input_data.get("start_time")
    end_time = input_data.get("end_time")
    transaction_id = input_data.get("transaction_id")
    from_address = input_data.get("from_address")
    to_address = input_data.get("to_address")

    record_query = record_query.order_by(TransferModel.id.desc())

    if limit and int(limit) > 0 and int(limit) <= 100:
        per_page = int(limit)
    else:
        per_page = 20

    if start_time:
        start_timestamp = int(datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S").timestamp())
        record_query = record_query.filter(TransferModel.create_time >= start_timestamp)
    if end_time:
        end_timestamp = int(datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S").timestamp())
        record_query = record_query.filter(TransferModel.create_time <= end_timestamp)

    if transaction_id:
        record_query = record_query.filter(TransferModel.transaction_id == transaction_id)
    if from_address:
        record_query = record_query.filter(TransferModel.from_address == from_address)
    if to_address:
        record_query = record_query.filter(TransferModel.to_address == to_address)

    record_query = record_query.paginate(page=current_page, per_page=per_page, error_out=False)

    return_data = {}
    return_data['total'] = record_query.total
    return_data['items'] = [temp.to_dict() for temp in record_query.items]

    return restful.ok(data=return_data)


@bp.route("/API_test", methods=['POST'])
def API_test():
    return_data = []
    try:
        if is_API_work('TRON'):
            return_data.append({'type': 'TRON', 'status': '成功'})
        else:
            return_data.append({'type': 'TRON', 'status': '失败'})
    except:
        return_data.append({'type': 'TRON', 'status': '失败'})

    return restful.ok(data=return_data)


@bp.route("/wallet", methods=['POST'])
def wallet():
    input_data = request.get_json()
    record_query = WalletModel.query
    limit = input_data.get("limit")
    current_page = input_data.get("page")

    address = input_data.get("address")

    record_query = record_query.order_by(*WalletModel.query_order())

    if limit and int(limit) > 0 and int(limit) <= 100:
        per_page = int(limit)
    else:
        per_page = 20

    if address:
        record_query = record_query.filter(WalletModel.address == address)

    record_query = record_query.paginate(page=current_page, per_page=per_page, error_out=False)

    return_data = {}
    return_data['total'] = record_query.total
    return_data['items'] = [temp.to_dict() for temp in record_query.items]

    return restful.ok(data=return_data)


@bp.route("/wallet_edit", methods=['POST'])
def wallet_edit():
    input_data = request.get_json()
    wallet_id = input_data.get('id')

    if not input_data.get('id'):
        return ""

    input_data.pop('id')
    WalletModel.query.filter(WalletModel.id == wallet_id).update(input_data)
    db.session.commit()

    return restful.ok()


@bp.route("/wallet_add", methods=['POST'])
def wallet_add():
    input_data = request.get_json()
    wallet_address = input_data.get('address').strip()
    wallet_type = input_data.get('type')
    wallet_priority = input_data.get('priority')
    wallet_secret = input_data.get('secret')

    wallet = WalletModel()
    wallet.address = wallet_address
    wallet.type = wallet_type
    wallet.priority = wallet_priority if wallet_priority else 0
    wallet.secret = wallet_secret if wallet_secret else None

    generate_QR_code(wallet_address)

    db.session.add(wallet)
    db.session.commit()

    return restful.ok()


@bp.route("/wallet_generate", methods=['POST'])
def wallet_generate():
    input_data = request.get_json()
    wallet_num = input_data.get('num')

    if not wallet_num or int(wallet_num) < 1 or int(wallet_num) > 1000:
        return restful.params_err()
    generate_wallet(wallet_num)

    return restful.ok()


@bp.route("/wallet_delete", methods=['POST'])
def wallet_delete():
    input_data = request.get_json()
    wallet_id = input_data['id']
    WalletModel.query.filter(WalletModel.id == wallet_id).delete()
    db.session.commit()

    return restful.ok()


@bp.route("/setting", methods=['POST'])
def setting():
    return_data = ConfigModel.get_all()

    return_data.pop('encrypt_key')

    return restful.ok(data=return_data)


@bp.route("/setting_edit", methods=['POST'])
def setting_edit():
    input_data = request.get_json()
    for key in input_data:
        ConfigModel.query.filter(ConfigModel.key == key).update({'value': input_data[key].strip()})

    db.session.commit()
    return restful.ok()


@bp.route("/log", methods=['POST'])
def log():
    log_path = "runtime/log/log"
    line_num = 100
    log_list = []
    if os.path.exists(log_path):
        with FileReadBackwards(log_path, encoding="utf-8") as f:
            for _ in range(line_num):
                line = f.readline()
                log_list.append(line)

    log_text = ''.join(log_list[::-1])
    return restful.ok(data=log_text)


@bp.route("/order_url_generate", methods=['POST'])
def order_url_generate():
    input_data = request.get_json()
    order_type = input_data.get('type')
    return_data = ""
    if order_type == 'epay':
        return_data = generate_epay_order_url()

    return restful.ok(data=return_data)
