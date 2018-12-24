# -*- coding: utf-8 -*-
# (C) shan weijia, 2018
# All rights reserved

'''Description '''

__author__ = 'shan weijia <shanweijia@jiaaocap.com>'
__time__ = '2018/12/24 9:12 AM'

from flask import Blueprint
from base.base_api import BaseApi
from global_reference import app

admin_buleprint = Blueprint("admin",__name__)
admin_api = BaseApi(admin_buleprint)
from . import admin
app.register_blueprint(admin_buleprint,url_prefix="/admin")