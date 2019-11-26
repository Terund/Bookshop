from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
import os
from flask_restful import Api
from flask_migrate import Migrate

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config.from_object("settings.Config")
# 让浏览器不显示unicode编码
app.config['JSON_AS_ASCII'] = False

models = SQLAlchemy()
api = Api()

migrate = Migrate(app, models)

def create():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config.from_object("settings.Config")
    app.config['JSON_AS_ASCII'] = False  # 让浏览器不显示unicode编码
    models.init_app(app)  # 加载数据库
    api.init_app(app)  # 加载restful插件
    from .main import main as main_project

    return app
