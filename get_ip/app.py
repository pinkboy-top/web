"""
公网ip查询模块，提供ip地址查询，ip详情查询
"""
import os
from datetime import datetime


from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from gevent.pywsgi import WSGIServer


from smtp_py import post_163_smtp
from ip_query import get_ip_info


app = Flask(__name__)
#  初始化数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + r'{}/{}'.format(os.path.abspath('.'), 'request_info.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'
db = SQLAlchemy(app)
# db.create_all()


#  数据模型
class RequestHost(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    host = db.Column(db.String(80), nullable=False)
    ua = db.Column(db.String(256), nullable=False)
    ip_info = db.Column(db.String(256), nullable=False)
    #  创建时间
    create_time = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, host, ua, ip_info):
        self.host = host
        self.ua = ua
        self.ip_info = ip_info


    def __repr__(self):
        return f'<host:{self.host},ua:{self.ua}>'


    def to_json(self):
         # 将db.Model 转化成json(特定方法)
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


@app.route('/get_ip', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        #  获取请求IP
        ip = request.remote_addr
        #  将获取的数据转成json
        data = request.get_json()
        #  查询所有的数据
        result = []
        try:
            flag = data.get('flag')
            page = data.get('page')
            if flag:
                pass
            for i in RequestHost.query.order_by(db.desc(RequestHost.id)).paginate(page=page, per_page=5, error_out=False).items:
                result.append(i.to_json())
            return jsonify({'msg': 'post', 'code': 200, 'request': result})
        except Exception as e:
            print(e)
            page = data.get('page')
            for i in RequestHost.query.order_by(db.desc(RequestHost.id)).paginate(page=page, per_page=5, error_out=False).items:
                result.append(i.to_json())
            return jsonify({'msg': 'post', 'code': 200, 'request': result})
    else:
        #  获取到的IP
        ip = request.remote_addr
        #  获取到的请求头
        ua = request.headers.get("User-Agent")
        #  获取ip详细信息
        ip_info = get_ip_info(ip)
        #  添加ip和ua到数据库
        add_data = RequestHost(ip, ua, ip_info)
        db.session.add(add_data)
        #  保存数据
        db.session.commit()
        return jsonify({'msg': 'get', 'code': 200, 'request': ip})


if __name__ == '__main__':
    db.create_all()
    # app.debug = False
    # app.run(host='0.0.0.0', port='9999')
    http_server = WSGIServer(('0.0.0.0', 9999), app)
    http_server.serve_forever()
