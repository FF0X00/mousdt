# from util.scheduler import start_wallet_job
import hashlib
import time

import base58
from cryptography.fernet import Fernet
# from util.scheduler import finish_job
from flask import g
from exts import db
from models import OrderModel, WalletModel, TransferModel, ConfigModel


def get_config(config_key: str):
    # 同一个context只查一次数据库
    if not g.get('config'):
        global_config = ConfigModel.get_all()
        g.config = global_config

    return g.config.get(config_key, None)


def free_wallet(contract_type='TRON'):
    result = WalletModel.query.filter(WalletModel.status == 1, WalletModel.type == contract_type).order_by(
        *WalletModel.query_order()).first()
    return result


def epay_sign(data):
    # 签名校验
    # 删除sign sign_type 空值
    sign_data = {}
    for dic_key in data.keys():
        if dic_key != 'sign' and dic_key != 'sign_type' and data[dic_key] is not None:
            sign_data[dic_key] = data[dic_key]

    # 将发送或接收到的所有参数按照参数名ASCII码从小到大排序（a-z），sign、sign_type、和空值不参与签名！
    sign_data = {k: v for k, v in sorted(sign_data.items())}

    # 将排序后的参数拼接成URL键值对的格式，例如 a=b&c=d&e=f，参数值不要进行url编码。
    param_string = "&".join([str(x) + "=" + str(sign_data[x]) for x in sign_data]) + get_config('epay_merchant_key')

    # 再将拼接好的字符串与商户密钥KEY进行MD5加密得出sign签名参数，sign = md5 ( a=b&c=d&e=f + KEY ) （注意：+ 为各语言的拼接符，不是字符！），md5结果为小写。
    return hashlib.md5(param_string.encode('utf-8')).hexdigest()


def clean_pending_order():
    # 标记超时订单
    # 注意这里，虽然订单创建在定时任务之前，但是由于时间精度问题，订单时间精度高，要加一秒增量
    OrderModel.query.filter((OrderModel.status == 0) & (OrderModel.end_time <= int(time.time()))).update({"status": -1})

    db.session.commit()


def clean_locked_wallet():
    # 标记超时钱包锁定
    WalletModel.query.filter((WalletModel.status == 0) & (WalletModel.end_lock_time <= time.time())).update(
        {'status': 1, 'end_lock_time': None, 'start_lock_time': None})
    db.session.commit()


def order_paid_amount(order_id):
    result = TransferModel.query.filter(TransferModel.order_id == order_id).all()

    receive_amount = 0
    for transfer in result:
        receive_amount += transfer.price
    return receive_amount


def encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)


def decrypt(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)


def generate_encrypt_key():
    return Fernet.generate_key()


def hex_to_base58(hex_string):
    if hex_string[:2] in ["0x", "0X"]:
        hex_string = "41" + hex_string[2:]
    bytes_str = bytes.fromhex(hex_string)
    base58_str = base58.b58encode_check(bytes_str)
    return base58_str.decode("UTF-8")


def base58_to_hex(base58_string):
    asc_string = base58.b58decode_check(base58_string)
    return asc_string.hex().upper()


def bordered_text(text):
    lines = text.splitlines()
    width = max(len(s) for s in lines)
    res = ['┌' + '─' * width + '┐']
    for s in lines:
        res.append('│' + (s + ' ' * width)[:width] + '│')
    res.append('└' + '─' * width + '┘')
    return '\n'.join(res)


def tron_address_to_parameter(addr):
    return "0" * 24 + base58.b58decode_check(addr)[1:].hex()


def refresh_wallet(wallet, force_refresh=False):
    from utils.api import get_tron_balance

    if not force_refresh:
        if wallet.refresh_time and wallet.refresh_time + int(get_config('wallet_refresh_cooldown_time')) > int(
                time.time()):
            return wallet

    balance = get_tron_balance(wallet.address)
    wallet.balance = balance
    wallet.refresh_time = int(time.time())
    db.session.commit()
    return wallet
