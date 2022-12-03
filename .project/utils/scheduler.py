import datetime
import time
from flask import current_app
import config
from create_app import create_app
from exts import cache
from exts import db
from exts import scheduler
from models import OrderModel, TransferModel, WalletModel
from utils.api import get_TRON_transfer_list
from utils.function import clean_pending_order, clean_locked_wallet, order_paid_amount


def start_scheduler():
    # 检查超时订单，检查超时锁定钱包，检查最新交易
    if not scheduler.get_job('check_job'):
        scheduler.add_job(check_job_with_context, 'interval', seconds=config.wallet_listener_interval, id="check_job")

    if not scheduler.get_job('clean_job'):
        start_date = datetime.datetime.now() + datetime.timedelta(seconds=int(config.wallet_listener_interval / 2))  # 报PytzUsageWarning
        scheduler.add_job(clean_job_with_context, 'interval', start_date=start_date,
                          seconds=config.wallet_listener_interval, id="clean_job")


def check_job_with_context():
    context_app = create_app()
    with context_app.app_context():
        try:
            check_job()
        except Exception as e:
            current_app.logger.exception(e)


def clean_job_with_context():
    context_app = create_app()
    with context_app.app_context():
        try:
            clean_job()
        except Exception as e:
            current_app.logger.exception(e)


def check_job():
    current_app.logger.debug('check_job')

    result = OrderModel.query.filter(OrderModel.status == 0).first()
    if not result:
        # 没有待支付订单则清除值，等待下一次开始订单
        cache.set('end_block_timestamp', None)
        return None

    # 获取时间范围内所有的交易，为防止错误及执行延迟，开始时间取上次的结束时间
    # 若上次结束时间没有设置，则说明是第一次进行，将开始时间往前倒一个周期
    # 每一次API获取成功后才设置结束时间，也就是说API请求报错也不会漏（报错出现在第一次则除外）
    # 此处问题是，若第一次执行时API报错，则不会设置结束时间，下一个周期结束时间还是没有设置，还会认为是第一次执行
    # 上次结束时间会在定时任务里面判断若无未付款订单则清空
    # 若启动时有未付款订单，则启动前这段时间的交易无法检测到会漏单
    start_block_timestamp = cache.get('end_block_timestamp')
    if not start_block_timestamp:
        start_block_timestamp = int((time.time() - config.wallet_listener_interval) * 1000)

    end_block_timestamp = int(time.time() * 1000)

    result = db.session.query(OrderModel.contract_type).group_by(OrderModel.contract_type).all()
    contract_type_list = [temp[0] for temp in result]

    transfer_list = []
    for contract_type in contract_type_list:
        if contract_type == 'TRON':
            current_app.logger.debug(
                f'query {contract_type} api {datetime.datetime.fromtimestamp(int(start_block_timestamp / 1000)).strftime("%m-%d %H:%M:%S")}-{datetime.datetime.fromtimestamp(int(end_block_timestamp / 1000)).strftime("%m-%d %H:%M:%S")}')
            transfer_list = get_TRON_transfer_list(start_block_timestamp=start_block_timestamp,end_block_timestamp=end_block_timestamp)
            # transfer_list = get_TRON_transfer_list(start_block_timestamp=1668788327000, end_block_timestamp=1668788329000)

    cache.set('end_block_timestamp', end_block_timestamp)

    if not transfer_list:
        return None

    # 对比数据库是否有对应的钱包地址
    address_list = [temp.to_address for temp in transfer_list]
    wallet_to_update_list = WalletModel.query.filter(WalletModel.address.in_(address_list)).all()

    if not wallet_to_update_list:
        return None

    # 找出待更新的钱包和对应的交易和对应的订单
    wallet_transfer_list = []
    for wallet in wallet_to_update_list:
        for transfer in transfer_list:
            if transfer.to_address == wallet.address:
                wallet_transfer_list.append({'wallet': wallet, 'transfer': transfer})

    # 添加交易到数据库,因为API的查询时间的问题可能会取到重复的交易记录，如果交易存在则从wallet_transfer_list删除
    for i in wallet_transfer_list[:]:
        result = TransferModel.query.filter(TransferModel.transaction_id == i['transfer'].transaction_id).first()
        if result:
            wallet_transfer_list.remove(i)
        else:
            db.session.add(i['transfer'])
            db.session.commit()

    # 找出相应的钱包、交易、订单，其中订单可能为空
    wallet_transfer_order_list = []
    for i in wallet_transfer_list:
        wallet = i['wallet']
        transfer = i['transfer']
        order = OrderModel.query.filter(
            (OrderModel.status == 0) &
            (OrderModel.wallet_id == wallet.id)
        ).first()
        wallet_transfer_order_list.append({'wallet': wallet, 'transfer': transfer, 'order': order})

    # 更新交易，将交易绑定到订单上，并找到对应订单的对应的钱包，并将余额加上
    for i in wallet_transfer_order_list:
        if i['order']:
            order = i['order']
            transfer = i['transfer']
            transfer.order = order

            order.paid_price += transfer.price
            order.wallet.balance += transfer.price
            db.session.commit()

    # 统计订单的金额，在时间范围内的交易
    # 若够数了，则订单完成，解锁钱包，更新订单，发送回调
    for i in wallet_transfer_order_list:
        if not i['order']:
            continue
        order = i['order']
        wallet = i['wallet']
        # result = TransferModel.query.filter( TransferModel.order == order).all()
        #
        # receive_amount = 0
        # for transfer in result:
        #     receive_amount += transfer.quant / 1e6
        receive_amount = order_paid_amount(order.id)

        # 由于是浮点数，为保险起见等于符号采用容差判断
        epsilon = 0.00005
        if abs(receive_amount - order.price) < epsilon or receive_amount > order.price:
            # 更新订单
            order.status = 1

            # 解锁钱包
            wallet.status = 1
            wallet.start_lock_time = None
            wallet.end_lock_time = None
            db.session.commit()

            # 发送回调
            order.notify()


# 订单超时，订单完成都会触发这个函数
def clean_job():
    current_app.logger.debug('clean job')
    # 标记超时订单,解锁钱包

    clean_pending_order()
    clean_locked_wallet()
