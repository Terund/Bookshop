import redis
import pymysql

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_restful import Api
# from flask_migrate import Migrate
from config import config_map

pymysql.install_as_MySQLdb()

db = SQLAlchemy()
api = Api()

# 创建redis连接对象
redis_store = None


# migrate = Migrate(app, models)

def create_app(config_name):
    # 根据配置模式的名字来获取模式的类
    app = Flask(__name__)
    config_class = config_map.get(config_name)
    app.config.from_object(config_class)
    app.jinja_env.auto_reload = True

    # 使用app来初始化db
    db.init_app(app)
    db.app = app  # 不加这句可能会报错

    # 初始化redis
    global redis_store
    redis_store = redis.StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT)

    # 利用flask-session将session数据保存到redis中
    Session(app)

    # 让浏览器不显示unicode编码
    app.config['JSON_AS_ASCII'] = False

    # 防止循环导包，延迟导入
    from shop import api_v1_0
    app.register_blueprint(api_v1_0)  # 注册蓝图

    return app
