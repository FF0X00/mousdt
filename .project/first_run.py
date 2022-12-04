import config
from create_app import create_app
from flask_sqlalchemy import inspect
from models import ConfigModel,AdminModel
import random
import string
from utils.function import bordered_text, generate_encrypt_key
from utils.tool.generate_wallet import generate_wallet
from exts import db, cache, scheduler, log_handler
import ntplib


def first_run(app):
    ntp_client = ntplib.NTPClient()
    rety_times = 0
    while True:
        try:
            response = ntp_client.request('cn.pool.ntp.org', version=3)
            break
        except Exception as e:
            if rety_times > 3:
                raise Exception(e)
            rety_times += 1

    time_offset = -response.offset
    if time_offset >= 0 and time_offset > config.wallet_listener_interval:
        raise Exception(f"Your system time is faster {time_offset} seconds, please sync time")

    if time_offset < 0 and -time_offset > config.wallet_listener_interval * 2:
        raise Exception(f"Your system time is slower {-time_offset} seconds, please sync time")

    # 创建默认表，写入默认数据
    context_app = create_app()

    with context_app.app_context():
        inspector = inspect(db.engine)

        if not inspector.has_table("config"):
            db.create_all()
            db.session.commit()

            epay_merchant_key = ''.join(random.choice(string.ascii_lowercase) for _ in range(16))
            db.session.add(ConfigModel(key='epay_merchant_key', value=epay_merchant_key))
            db.session.add(ConfigModel(key='order_duration', value='900'))
            db.session.add(ConfigModel(key='wallet_refresh_cooldown_time', value='100'))
            db.session.add(ConfigModel(key='encrypt_key', value=generate_encrypt_key().decode()))
            db.session.add(ConfigModel(key='trongrid_key', value=''))

            admin_password = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
            db.session.add(AdminModel(username='admin', password=admin_password))

            print(bordered_text(f'  Login Info\nusername:admin\npassword:{admin_password}\nepay_merchant_key:{epay_merchant_key}\n\n!!!This message is only shown once!!!'))
            db.session.commit()

            generate_wallet()

    cache.set('end_block_timestamp', None)

    # # 不应写在create_app，当create_app被调用一次就会新创建一个log实例，导致出现重复日志
    app.logger.addHandler(log_handler())

    # 创建定时任务
    from utils.scheduler import start_scheduler
    start_scheduler()
    scheduler.start()

    return app
