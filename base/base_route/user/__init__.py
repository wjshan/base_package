# -*- coding: utf-8 -*-
# (C) shan weijia, 2018
# All rights reserved

'''Description '''

__author__ = 'shan weijia <shanweijia@jiaaocap.com>'
__time__ = '2018/12/14 4:46 PM'

from flask import Blueprint
from base.base_api import BaseApi
from global_reference import app

user_buleprint = Blueprint("user",__name__)
user_api = BaseApi(user_buleprint)
from . import user
app.register_blueprint(user_buleprint,url_prefix="/user")