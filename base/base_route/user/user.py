# -*- coding: utf-8 -*-
# (C) shan weijia, 2018
# All rights reserved

'''Description '''

__author__ = 'shan weijia <shanweijia@jiaaocap.com>'
__time__ = '2018/12/14 4:42 PM'

from . import user_api
from flask_restful import Resource
from base.base_model.model_user import User
from flask import request

from base.help.http_error_code import retrun_error
from global_reference import db
import hashlib
from sqlalchemy import or_

from base.help import token
from base.help.flask_params import Rules, Rule, rule_len, email
from functools import partial


@user_api.resource("/login")
class UserLogin(Resource):
    def post(self):
        user_name = request.form.get("user_name", "")
        passwd = request.form.get("passwd", "")
        if not user_name:
            raise retrun_error(1001)
        user_recode = db.session.query(User.name, User.passwd,User.is_use).filter(User.name == user_name).one_or_none()
        if user_recode is None:  # 检测用户是否存在
            return retrun_error(1003)
        if not user_recode.is_use: # 检测用户是否被激活
            return retrun_error(1004)
        passwd_md5 = hashlib.new("md5", passwd.encode()).hexdigest()
        if passwd_md5 != user_recode.passwd:  # 校验密码
            return retrun_error(1002)
        return {"access_token": token.get_token({"name": user_name})}


@user_api.resource("/register")
class UserRegister(Resource):
    nickname_rule = partial(Rule, field="nickname", location=("form", "json"), rule_funcs=[rule_len(6, 20)],
                            error_func=user_api.error_func, require=True, nullable=False)
    email_rule = partial(Rule, field="email", location=("form", "json"), rule_funcs=[email],
                         error_func=user_api.error_func, require=True, nullable=False)
    password_rule = partial(Rule, field="password", location=("form", "json"), rule_funcs=[rule_len(6, 12)],
                            error_func=user_api.error_func, require=True, nullable=False)
    repass_rule = partial(Rule, field="repass", location=("form", "json"), rule_funcs=[rule_len(6, 12)],
                          error_func=user_api.error_func, require=True, nullable=False)

    def post(self):
        params = Rules(self.nickname_rule(), self.email_rule(), self.password_rule(), self.repass_rule()).run()
        if params["password"] != params["repass"]:
            return retrun_error(3001)
        pwd_md5 = hashlib.new("md5", params["password"].encode()).hexdigest()

        already_user = db.session.query(User.name, User.email).filter(
            or_(User.name == params["nickname"], User.email == params["email"])).one_or_none()
        if already_user is not None:
            if already_user.name == params["nickname"]:
                return retrun_error(3002,message="用户{0}已注册".format(params["nickname"]))
            if already_user.email == params["email"]:
                return retrun_error(3003, message="邮箱{0}已注册".format(params["email"]))
            return retrun_error(3004)
        user = User(name=params["nickname"], passwd=pwd_md5, email=params["email"])
        db.session.add(user)
        db.session.commit()
        return "用户{0}创建完成".format(params["nickname"])
