from main import app, api
from flask import render_template
from flask import request, redirect, session, jsonify
from models import *
from flask_restful import Resource
import functools
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import time

address = "10.10.16.162:6379:123456:bigproject"


def genTokenSeq(name, passwd, address, expires=300):
    '''
    加密数据为jwt字符串
    :param name: 用户名
    :param passwd: 用户密码
    :param address: 服务器地址
    :param expires: 过期时间，默认5分钟，单位：秒
    :return: 返回字节流字符串
    salt:随机字符串，默认不可变，更改需要与服务器沟通
    secret_key:秘钥，默认不可变，更改需要与服务器沟通
    '''
    s = Serializer(
        salt='16fcf475-5180-4916-83c1-5ff79616eaa9',
        secret_key='4180da82-0c83-4d66-ab14-e2793573ecaa',
        expires_in=expires
    )
    timestamp = time.time()
    json_str = {
        'user_name': name,
        'user_passwd': passwd,
        'user_address': address,
        'timeout': expires,
        'iat': timestamp
    }
    return s.dumps(json_str).decode('utf-8')


def loginValid(fun):
    functools.wraps(fun)  # 保留原函数的名称

    def inner(*args, **kwargs):
        cookie_email = request.cookies.get("email")
        cookie_id = request.cookies.get("id")
        if cookie_id:
            user = Userinfo.query.get(int(cookie_id))
            session_password = session.get("password")
            if user.email == cookie_email and user.password == session_password:
                return fun(*args, **kwargs)
        return redirect("/login/")

    return inner


@app.route("/")
def index():
    return render_template("index.html", **locals())


@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form_data = request.form
        email = form_data.get("exampleInputEmail1")
        password = form_data.get("exampleInputPassword1")
        if email and password:
            user = Userinfo.query.filter_by(user_name=email).first()
            if user.user_name == email:
                if user.password == password:
                    token = genTokenSeq(email, password, address)
                    response = jsonify({"token": token})
                    response.set_cookie("id", str(user.id))
                    response.set_cookie("email", user.email)
                    session["password"] = user.password
                    return response
    return jsonify({"error": "密码错误"})


@app.route("/logout/")
def logout():
    response = redirect("/login/")
    response.delete_cookie("id")
    response.delete_cookie("email")
    session.pop("password")
    # del session["password]  # 另一种session删除方法
    return response


@app.route("/base/")
def base():
    return render_template("base.html")


@app.route("/about/")
def about():
    return render_template("about.html")


@app.route("/all-brands/")
def all_brands():
    return render_template("all-brands.html")


@app.route("/blog/")
def blog():
    return render_template("blog.html")


@app.route("/blog-post/")
def blog_post():
    return render_template("blog-post.html")


@app.route("/books/")
def books():
    return render_template("books.html")


@app.route("/categories/")
def categories():
    return render_template("categories.html")


@app.route("/contact/")
def contact():
    return render_template("contact.html")


@app.route("/error/")
def error():
    return render_template("error.html")


@app.route("/home/")
def home():
    return render_template("home.html")


@app.route("/ihome/")
def ihome():
    return render_template("ihome.html")


@app.route("/magazine/")
def magazine():
    return render_template("magazine.html")


@app.route("/single-book/")
def single_book():
    return render_template("single-book.html")


@api.resource("/api/books/")
class BookApi(Resource):
    def __init__(self):
        super(BookApi, self).__init__()
        self.result = {
            "Code": 200,
            "Version": "v1.0",
        }

    def set_data(self, books):
        result_data = {
            "id": books.id,
            "title": books.title,
            "detail_description": books.detail_description,
            "picture": books.picture,
            "author": books.author,
            "publish_time": books.publish_time,
            "price": books.price,
            "type": Types.query.get(books.type_id).type
        }
        return result_data

    def get(self):
        """
        从数据库中获取数据
        :return: 返回获取到的数据，200：获取成功，400：获取失败
        """
        self.result["Method"] = "get"
        columns = ["start_page", "limit", "start"]
        data = request.args
        if data:
            self.result["Code"] = 200
            self.result["Message"] = "获取数据成功"
            limit = int(data.get("limit", 10))
            start_page = (int(data.get("start_page", 1)) - 1 if (int(data.get("start_page", 1)) > 0) else 0) * limit
            start = int(data.get("start", 1)) - 1 if (int(data.get("start", 1)) > 0) else 0
            if data.get("start"):
                id_list = Books.query.with_entities(Books.id).all()[start:start + limit]
            else:
                id_list = Books.query.with_entities(Books.id).all()[start_page:start_page + limit]
            page_range = [i[0] for i in id_list]
            books = Books.query.filter(Books.id.in_(page_range)).all()
            book_list = []
            for book in books:
                book_list.append(self.set_data(book))
            self.result["Data"] = book_list
        else:
            books = Books.query.with_entities(Books.id).all()
            total = len(books)
            self.result["Code"] = 200
            self.result["Total"] = total
            self.result["Columns"] = columns
        return jsonify(self.result)

    def post(self):
        """
        这里是post请求，负责保存数据
        :return: 返回数据保存的状态，201：保存成功，400：保存失败
        """
        self.result["Method"] = "post"
        columns = sorted(["title", "detail_description", "picture", "author", "publish_time", "price", "type"])
        data = request.form
        columns_post = [i for i in data]
        columns_post.sort()
        if data:
            if columns != columns_post:
                self.result["Code"] = 400
            else:
                self.result["Code"] = 201
                self.result["Message"] = "增加数据成功"
                session = models.session()
                session.add(Books(
                    author=data.get("author"),
                    detail_description=data.get("detail_description"),
                    picture=data.get("picture"),
                    price=data.get("price"),
                    publish_time=data.get("publish_time"),
                    title=data.get("title"),
                    type_id=Types.query.filter_by(type=data.get("type")).first().id,
                ))
                session.commit()
        else:
            self.result["Code"] = 400
            self.result["Columns"] = columns
            self.result["Message"] = "增加数据失败"
        return jsonify(self.result)

    def put(self):
        """
        负责修改数据
        :return:返回修改的状态，201：修改成功，400：修改失败
        """
        self.result["Method"] = "put"
        data = request.form
        columns = sorted(["id", "title", "detail_description", "picture", "author", "publish_time", "price", "type"])
        columns_put = [i for i in data]
        if "id" in columns_put and set(columns) >= set(columns_put):
            self.result["Code"] = 201
            self.result["Message"] = "修改数据成功"
            id = int(data.get("id"))
            book = Books.query.get(id)
            for key, value in data.items():
                if key not in ["id", "type"]:
                    setattr(book, key, value)
            book.type_id = int(data.get("type", book.type_id))
            book.save()
        else:
            self.result["Code"] = 400
            self.result["Columns"] = columns
            self.result["Message"] = "修改数据失败"
        return jsonify(self.result)

    def delete(self):
        """
        负责删除数据
        :return: 返回删除的状态，204：删除成功，400：删除失败
        """
        data = request.form
        self.result["Method"] = "delete"
        if data == ["id"]:
            self.result["Code"] = 204
            self.result["Message"] = "删除数据成功"
            id = int(data.get("id"))
            book = Books.query.get(id)
            book.delete()
        else:
            self.result["Code"] = 400
            self.result["Columns"] = ["id"]
            self.result["Message"] = "删除数据失败"
        return jsonify(self.result)
