# -*- coding: utf-8 -*-
# (C) shan weijia, 2018
# All rights reserved

'''Description 在此实例化全局引用的内容，例如全局的数据库连接配置'''

__author__ = 'shan weijia <shanweijia@jiaaocap.com>'
__time__ = '2018/11/9 4:02 PM'

import os
from flask import Flask, request
import json

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
    "SQLALCHEMY_TRACK_MODIFICATIONS": False
})

# 加载用户配置
app.config.from_pyfile("default_config.py")


def get_env(name, default=None):
    if name in os.environ:
        return os.environ[name]
    elif name in app.config:
        return app.config[name]
    else:
        return default


# 初始化数据库
from flask_sqlalchemy import SQLAlchemy

# 将pymysql映射成MySQLdb
from pymysql import install_as_MySQLdb

install_as_MySQLdb()

db = SQLAlchemy(app, session_options={"autocommit": False, "autoflush": False, })


# 全局自定义错误类
class HttpError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return "{0}-{1}".format(self.code,self.message)


import traceback


def module_load():
    for user_module in _get_modules_path():
        try:
            __import__(user_module)
        except ImportError:
            traceback.print_exc()
    return


def _get_modules_path():
    return ["base." + path for path in os.listdir("base") if
            os.path.isdir("base/" + path) and ("." not in path)]


module_load()
