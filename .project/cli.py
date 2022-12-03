from flask import Flask
import click
from models import AdminModel
from utils.function import bordered_text
from exts import db
import os
import shutil


def register_cli(app: Flask):
    @app.cli.command('admin', with_appcontext=True)
    @click.option('--username', type=str, default='admin', help='Amin username')
    @click.option('--password', type=str, required=True, help='Amin password')
    def admin(username, password):
        if password == 'admin':
            print(bordered_text(' Please change a stronger password! '))
            return 0
        AdminModel.query.filter(AdminModel.id == 1).first().username = username
        AdminModel.query.filter(AdminModel.id == 1).first().password = password
        db.session.commit()

        print(bordered_text(f'   success\nusername:{username} \npassword:{password} '))

    @app.cli.command('clear_data')
    def clear_data():
        current_dir = os.path.dirname(os.path.realpath(__file__))
        runtime_path = os.path.join(current_dir, 'runtime')
        sqlite_path = os.path.join(current_dir, 'database.db')
        QR_code_path = os.path.abspath(os.path.join(current_dir,"..","static","QR_code"))


        try:
            os.remove(sqlite_path)
            print(sqlite_path)
        except:
            pass

        try:
            shutil.rmtree(runtime_path)
            print(runtime_path)
        except:
            pass

        try:
            shutil.rmtree(QR_code_path)
            print(QR_code_path)
        except:
            pass


