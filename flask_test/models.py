from main import models


class BaseModel(models.Model):
    __abstract__ = True  # 声明当前类为抽象类，被继承调用不被创建
    id = models.Column(models.Integer, primary_key=True, autoincrement=True)

    def save(self):
        db = models.session()
        db.add(self)
        db.commit()

    def delete(self):
        db = models.session()
        db.delete(self)
        db.commit()


class Userinfo(BaseModel):
    __bind_key__ = "bigproject"
    __tablename__ = "userinfo"
    id = models.Column(models.Integer, primary_key=True)
    user_name = models.Column(models.String(32))
    user_passwd = models.Column(models.String(32))


class Books(BaseModel):
    __bind_key__ = "dangdangdata"
    __tablename__ = "books"
    id = models.Column(models.Integer, primary_key=True)
    title = models.Column(models.String(255))
    detail_description = models.Column(models.String(1024))
    picture = models.Column(models.String(255))
    author = models.Column(models.String(255))
    publish_time = models.Column(models.String(255))
    price = models.Column(models.String(10))
    type_id = models.Column(models.Integer)


class Types(BaseModel):
    __bind_key__ = "dangdangdata"
    __tablename__ = "types"
    id = models.Column(models.Integer, primary_key=True)
    type = models.Column(models.String(255))
