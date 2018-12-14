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
})

from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] = "sqllit:///temp_db/test.db"  # 配置数据库连接地址
db = SQLAlchemy(app, session_options={"autocommit": False, "autoflush": False, })

# celery 配置
from celery import Celery, platforms
from celery.utils.log import get_task_logger
from kombu import Exchange, Queue
from kombu.serialization import registry
from datetime import datetime, date
import dateutil.parser





class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return {"val": obj.isoformat(), "_spec_type": "datetime"}
        elif isinstance(obj, date):
            return {"val": obj.isoformat(), "_spec_type": "date"}
        else:
            return json.JSONEncoder.default(self, obj)


def date_time_hook(obj):
    _spec_type = obj.get('_spec_type')
    if not _spec_type:
        return obj
    if _spec_type in CONVERTERS:
        return CONVERTERS[_spec_type](obj['val'])
    else:
        raise Exception('Unknown {}'.format(_spec_type))


CONVERTERS = {
    'datetime': dateutil.parser.parse,
    'date': dateutil.parser.parse,
}





def register_jsond():
    def dumps(*args, **kwargs):
        return json.dumps(*args, **dict(kwargs, cls=CJsonEncoder))

    def loads(*args, **kwargs):
        args = [x.decode() if isinstance(x, bytes) else x for x in args]
        return json.loads(*args, **dict(kwargs, object_hook=date_time_hook))

    registry.register('jsond', dumps, loads,
                      content_type='application/json',
                      content_encoding='utf-8')


platforms.C_FORCE_ROOT = True
register_jsond()
celery = Celery(__name__)
logger = get_task_logger(__name__)

# if get_env("START_METHOD") == "heartbeat":
#     queues = [Queue('olympus_heartbeat', Exchange('olympus_heartbeat'), routing_key='olympus_heartbeat',
#                     consumer_arguments={'x-max-priority': 10}), ]
# else:
#     queues = [Queue('index_compute_server', Exchange('index_compute_server'), routing_key='index_compute_server',
#                     consumer_arguments={'x-max-priority': 10}), ]
queues = [Queue('heartbeat', Exchange('heartbeat'), routing_key='heartbeat',
                    consumer_arguments={'x-max-priority': 10}), ]

CELERY_TASK_SERIALIZER = 'jsond'
CELERY_RESULT_SERIALIZER = 'jsond'
CELERY_TASK_RESULT_EXPIRES = 30
CELERY_ACCEPT_CONTENT = ["json", 'json']
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERYD_FORCE_EXECV = True
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 24 * 60 * 60}
CELERY_IGNORE_RESULT = False
CELERYD_CONCURRENCY = 20  # 并发worker数
CELERYD_TASK_SOFT_TIME_LIMIT = 60 * 60 * 24
CELERYD_TASK_TIME_LIMIT = 60 * 60 * 24
CELERYD_PREFETCH_MULTIPLIER = 1
celery.conf.update({
    "BROKER_HOST": "127.0.0.1",
    "BROKER_PORT": "5672",
    "BROKER_USER": "admin",
    "BROKER_PASSWORD": "admin",
    "BROKER_VHOST": "/",
    "CELERY_RESULT_BACKEND": 'redis://{host}:{port}/{db}'.format(host="127.0.0.1",
                                                                 port="6379",
                                                                 db="3"),
    "CELERY_TASK_SERIALIZER": CELERY_TASK_SERIALIZER,
    "CELERYD_prefetch_multiplier": CELERYD_PREFETCH_MULTIPLIER,
    "CELERY_RESULT_SERIALIZER": CELERY_RESULT_SERIALIZER,
    "CELERY_TASK_RESULT_EXPIRES": CELERY_TASK_RESULT_EXPIRES,
    "CELERY_ACCEPT_CONTENT": CELERY_ACCEPT_CONTENT,
    "CELERY_TIMEZONE": CELERY_TIMEZONE,
    "BROKER_TRANSPORT_OPTIONS": BROKER_TRANSPORT_OPTIONS,
    "CELERY_IGNORE_RESULT": CELERY_IGNORE_RESULT,
    "CELERYD_CONCURRENCY": CELERYD_CONCURRENCY,
    "CELERY_QUEUES": queues
})
