import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_FILES = os.path.join(BASE_DIR, "static")

# 设置连接多个数据库
SQLALCHEMY_BINDS = {
    "bigproject": "mysql+mysqlconnector://root:123456@localhost:3306/bigproject",
    "dangdangdata": "mysql+mysqlconnector://root:7890@39.107.253.135:33060/dangdangdata"
}


class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:123456@localhost/bigproject"
    SQLALCHEMY_BINDS = SQLALCHEMY_BINDS
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True


class RunConfig(Config):
    DEBUG = False
