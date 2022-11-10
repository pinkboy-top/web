# 获取B站宅舞区的4k视频图片信息保存或返回图片链接.
import random
from datetime import datetime
from typing import List, Iterator
import os

import requests
from flask import Flask, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
#  初始化数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + r'{}/{}'.format(os.path.abspath('.'), 'info.db')
db = SQLAlchemy(app)


#  B站up主数据模型
class UPInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    uid = db.Column(db.Integer, unique=True, nullable=False)
    mid = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(128), nullable=False)
    pic = db.Column(db.String(256), nullable=False)
    title = db.Column(db.String(256), nullable=False)
    tag = db.Column(db.String(256), nullable=False)
    description = db.Column(db.String(512), nullable=False)
    #  创建时间
    create_time = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, uid, mid, url, pic, title, tag, description):
        self.uid = uid
        self.mid = mid
        self.url = url
        self.pic = pic
        self.title = title
        self.tag = tag
        self.description = description

    def __repr__(self):
        return f'<title:{self.title}>'

    def to_json(self):
        # 将db.Model 转化成json(特定方法)
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
}


def get_img(url: str) -> [List]:
    """
    :param url: 需要抓取的目标接口
    :return: 图片的列表
    """
    # 请求查询接口处理返回图片链接
    req_data = requests.get(url, headers=headers).json()
    result = req_data.get('data').get('result')
    info_list = []
    for val in result:
        info_list.append({"uid": val.get('id'), "mid": val.get('mid'), "url": val.get('arcurl'), "pic": val.get('pic'),
                          "title": val.get('title'), "tag": val.get('tag'), "description": val.get('description')})
    return info_list


def save_data(data: list) -> Iterator:
    """
    # 保存获取到的数据
    :param data: up主信息列表
    :return: 状态码
    """
    #  添加获取的数据到数据库
    try:
        for val in data:
            add_data = UPInfo(
                val.get('uid'), val.get('mid'), val.get('url'), val.get('pic'), val.get('title'), val.get('tag'),
                val.get('description')
            )
            db.session.add(add_data)
            #  保存数据
            db.session.commit()
        return 0
    except IntegrityError:
        return 1


@app.route('/get_img', methods=['GET', 'POST'])
def index():
    """
    获取图片接口
    :return:
    """
    if request.method == 'POST':
        # 获取需要抓取的页码
        data = request.get_json()
        page_index = data.get('page')
        if page_index:
            result = get_img(
                f"https://api.bilibili.com/x/web-interface/search/type?context=&page={page_index}&order=click&keyword=4"
                f"k&duration=1&from_source=video_tag&from_spmid=333.788.b_765f746167.13&platform=pc&__refresh__=true"
                f"&_extra=&search_type=video&tids=20&highlight=1&single_column=0")
            if result:
                #  添加获取的数据到数据库
                save_data(result)
                return jsonify({'msg': 'save ok', 'code': 100})

        else:
            return jsonify({'msg': 'no page', 'code': -1})
    else:
        # 获取翻页
        data = request.get_json()
        page = None
        try:
            page = data.get('page')
        except AttributeError:
            pass
        if page:
            cache = []
            for val in UPInfo.query.order_by(db.desc(UPInfo.id)).paginate(page=page, per_page=20, error_out=False).items:
                cache.append(val.to_json())
            return jsonify({'msg': 'ok', 'code': 200, 'data': cache})
        else:
            cache = []
            for val in UPInfo.query.all():
                cache.append(val.to_json())
            rest_url = random.choice(cache).get('pic')
            # return jsonify({'msg': 'ok', 'code': 200, 'data': random.choice(cache)})
            return redirect(rest_url)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    db.create_all()
    app.debug = True
    app.run(host='0.0.0.0', port='9090')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
