from flask import Flask, has_app_context, g
import config
from exts import db, scheduler, jwt, cache, log_handler, limiter
from first_run import first_run
from flask_migrate import Migrate  # MigrateCommand报错的话要降级安装2.7
import models  # 虽然没有使用，但是需要在migrate所在文件导入，这样migrate才能识别
from models import *
import os
from flask_sqlalchemy import inspect
import string
import random
from create_app import create_app
from cli import register_cli

app = create_app()
migrate = Migrate(app, db, compare_type=True, render_as_batch=True)  # sqlite不支持直接修改列属性，render_as_batch是复制现有表数据并填入新表
register_cli(app)

# FLASK_ENV判断是否是调试环境, FLASK_DEBUG判断pycharm是否关闭reloader运行,WERKZEUG_RUN_MAIN判断是否是reloader
if os.environ.get('FLASK_ENV') != 'development' or os.environ.get('FLASK_DEBUG') == '0' or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    first_run(app)


@app.route('/')
def index():
    print(test1)
    return 'Hello'


if __name__ == '__main__':
    app.run()
