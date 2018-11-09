# -*- coding: utf-8 -*-
# (C) shan weijia, 2018
# All rights reserved

'''Description 在此实例化全局引用的内容，例如全局的数据库连接配置'''

__author__ = 'shan weijia <shanweijia@jiaaocap.com>'
__time__ = '2018/11/9 4:02 PM'

import os
from flask import Flask, request

# 实例化Flask类
app = Flask(__name__)


@app.before_request
def before_request():
    '''注册在请求响应之前的方法
    将template与static修改到jinja的查找路径中
    '''
    if request.blueprint is not None:
        bp = app.blueprints[request.blueprint]
        if bp.jinja_loader is not None:
            newsearchpath = bp.jinja_loader.searchpath + app.jinja_loader.searchpath
            app.jinja_loader.searchpath = newsearchpath
        else:
            app.jinja_loader.searchpath = app.jinja_loader.searchpath[-1:]
    else:
        app.jinja_loader.searchpath = app.jinja_loader.searchpath[-1:]


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
app.config.from_mapping({
    "APP_NAME": "main",
    "PROJECT": "app",
    "PROJECT_ROOT": os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
    "LOG_FOLDER": os.path.join(PROJECT_ROOT, 'log'),
    "SECRET_KEY": os.urandom(24),
})

from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] = "sqllit:///temp_db/test.db"  # 配置数据库连接地址
db_model = SQLAlchemy(app)



