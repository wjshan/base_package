# -*- coding: utf-8 -*-
# (C) shan weijia, 2018
# All rights reserved

'''Description '''

__author__ = 'shan weijia <shanweijia@jiaaocap.com>'
__time__ = '2018/12/17 2:03 PM'

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import JSONWebSignatureSerializer
from functools import wraps
from .http_error_code import retrun_error
import traceback
from flask import current_app

from global_reference import get_env


def get_token(message, expires=None):
    '''
    :param message: 生成token的数据，后续可以解析
    :param expires: 超时时间 默认3600秒
    :return:
    '''
    s = Serializer(secret_key=get_env("SECRET_KEY"), salt=get_env("SALT"), expires_in=expires)
    return s.dumps(message).decode()


class TokenAuth(Serializer):
    def __init__(self, token_func=None, token_name=None, bind=True):
        super(TokenAuth, self).__init__(secret_key=get_env("SECRET_KEY"), salt=get_env("SALT"))
        self.token_func = token_func
        self.token_name = token_name or "access_token"
        self.bind = bind

    def loads_token(self, token):
        try:
            payload, header = JSONWebSignatureSerializer.loads(self, token, return_header=True)
            if 'exp' not in header:
                retrun_error(4001)
            if not (isinstance(header['exp'], int) and header['exp'] > 0):
                retrun_error(4002)
            if header['exp'] < self.now():
                retrun_error(4003)
            return payload
        except:
            traceback.print_exc()
            retrun_error(4004)

    def __call__(self, func):
        @wraps(func)
        def call(*args, **kwargs):
            if callable(self.token_func):
                token = self.token_func(self.token_name)
            else:
                token = self.token_func
            if not token:
                return retrun_error(4005)
            payload = self.loads_token(token)
            if payload is None:
                retrun_error(4005)
            if self.bind:
                return func(*args, payload=payload, **kwargs)
            else:
                return func(*args, **kwargs)

        return call
