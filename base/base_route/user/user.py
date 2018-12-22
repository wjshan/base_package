# -*- coding: utf-8 -*-
# (C) shan weijia, 2018
# All rights reserved

'''Description '''

__author__ = 'shan weijia <shanweijia@jiaaocap.com>'
__time__ = '2018/12/14 4:42 PM'

from . import user_api
from flask_restful import Resource
from base.base_model.model_user import User
from flask_restful import request

from base.help.http_error_code import retrun_error
from global_reference import db
import hashlib

from base.help import token


@user_api.resource("/login")
class user_login(Resource):
    def post(self):
        user_name = request.form.get("user_name", "")
        passwd = request.form.get("passwd", "")
        if not user_name:
            raise retrun_error(1001)
        user_recode = db.session.query(User.name, User.passwd).filter(User.name == user_name).one_or_none()
        if user_recode is None:
            return retrun_error(1003)
        passwd_md5 = hashlib.new("md5", passwd.encode()).hexdigest()
        if passwd_md5 != user_recode.passwd:
            return retrun_error(1002)
        return {"token":token.get_token({"name":user_name})}



