import os
import redis

# 项目的根目录
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# 模板文件目录
TEMPLATES_FOLDER = os.path.join(BASE_DIR, "templates")
# 静态文件目录
STATIC_FOLDER = os.path.join(BASE_DIR, "static")


class Config(object):
    # 设置一个随机值
    SECRET_KEY = os.urandom(24)

    # MySQL数据库配置
    SQLALCHEMY_BINDS = {
        "bigproject": "mysql+mysqlconnector://root:123456@localhost:3306/bigproject",
        "dangdangdata": "mysql+mysqlconnector://root:7890@39.107.253.135:33060/dangdangdata"
    }
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:123456@localhost/bigproject"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # redis配置
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # flask-session的配置
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True  # 对cookie中的session_id设置隐藏处理
    PERMANENT_SESSION_LIFETIME = 86400  # session数据的有效期，单位：秒
    # 模板热加载
    TEMPLATES_AUTO_RELOAD = True


class DevelopmentConfig(Config):
    DEBUG = True


class ProjectionConfig(Config):
    pass


config_map = {
    "develop": DevelopmentConfig,
    "product": ProjectionConfig
}
