# This is a sample Python script.
# 李子树秘密岛.
import random
from datetime import datetime
from typing import List, Iterator
import os
from urllib import parse
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import requests
from flask import Flask, request, jsonify, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from gevent.pywsgi import WSGIServer

app = Flask(__name__)
#  初始化数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + r'{}/{}'.format(os.path.abspath('.'), 'info.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
db = SQLAlchemy(app)


#  秘密数据模型
class MsgInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nickname = db.Column(db.String(256), nullable=False)
    content = db.Column(db.String(512), nullable=False)
    anonymous = db.Column(db.Integer, default=1)
    tag = db.Column(db.String(256), default="默认标签", nullable=False)
    views = db.Column(db.Integer, default=1)
    # 创建时间
    create_time = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, nickname, content):
        self.nickname = nickname
        self.content = content

    def __repr__(self):
        return f'<title:{self.nickname}>'

    def to_json(self):
        # 将db.Model 转化成json(特定方法)
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
    "Host": "api.zhishishijian.com",
    "Origin": "http://wx.shanzhadao.com",
    "Referer": "http://wx.shanzhadao.com/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
}


def get_msg(name: str) -> dict:
    """
    # 获取接口的第三方信息
    :param name:
    :return:
    """
    flag = parse.quote(name)
    url = f"http://api.zhishishijian.com/api/info/get_infos_shanzha_by_watchword_lite?watchword={flag}"
    cache = requests.get(url, headers=headers)
    if cache:
        result = cache.json()
        return result
    else:
        return {"msg": "error", "code": -1}


def save_data(data: list) -> int:
    """
    # 保存获取到的数据
    :param data: 信息列表
    :return: 状态码
    """
    #  添加获取的数据到数据库
    try:
        for val in data:
            add_data = MsgInfo(
                val.get('nickname'), val.get('content')
            )
            db.session.add(add_data)
            #  保存数据
            db.session.commit()
        return 0
    except IntegrityError:
        return 1


@app.route('/home', methods=['GET', 'POST'])
def home(name=None):
    """
    :return: template
    """
    if request.method == 'POST':
        name = request.form['name']
        if len(MsgInfo.query.filter_by(nickname=name).all()) == 0:
            # 数据库没有数据就去接口取取完入库保存
            result = "没有数据"
            return render_template("index.html", name=result)
        else:
            result = MsgInfo.query.filter_by(nickname=name).all()
            return render_template("index.html", name=result)
    else:
        return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add(msg=None):
    """
    :return: template
    """
    if request.method == 'POST':
        name = request.form['name']
        content = request.form['content']
        if name and content:
            if save_data([{"nickname": name, "content": content}]) == 0:
                return render_template("add.html", msg="成功")
            else:
                return render_template("add.html", msg="添加失败!")
        else:
            return render_template("add.html", msg="没有数据!")
    else:
        return render_template("add.html", msg="flag")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    db.create_all()
    app.debug = False
    http_server = WSGIServer(('0.0.0.0', 8888), app)
    http_server.serve_forever()
