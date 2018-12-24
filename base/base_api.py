# -*- coding: utf-8 -*-
# (C) shan weijia, 2018
# All rights reserved

'''Description '''

__author__ = 'shan weijia <shanweijia@jiaaocap.com>'
__time__ = '2018/12/22 8:48 PM'
from flask_restful import Api
from flask import jsonify
from global_reference import HttpError, db
from base.help.http_error_code import retrun_error
from flask.app import MethodNotAllowed
from base.help.flask_params import ArgumentError
import traceback


class BaseApi(Api):
    def handle_error(self, e):
        try:
            if isinstance(e, HttpError):
                return self.error_response(code=e.code, message=e.message)
            elif isinstance(e, MethodNotAllowed):
                return self.error_response(code=405, message="未经允许的访问方式")
            traceback.print_exc()
            return self.error_response(code=500, message=str(e))
        finally:
            db.session.rollback()
            db.session.close()

    def error_response(self, code, message):
        return jsonify({"code": code, "message": message, "data": None})

    def make_response(self, data, *args, **kwargs):
        try:
            default = {"code": 200, "message": "请求成功", "data": data}
            resp = super(BaseApi, self).make_response(default, *args, **kwargs)
            return resp
        finally:
            db.session.rollback()
            db.session.close()

    @staticmethod
    def error_func(e: ArgumentError):
        if e.flag == "not_fund":
            return retrun_error(2001, message="缺少必填参数{0}".format(e.field))
        elif e.flag == "type_error":
            return retrun_error(2002, message="参数{0}不合法,检测失败".format(e.field))
        else:
            return retrun_error(2003, message="参数{0}不允许为空".format(e.field))
