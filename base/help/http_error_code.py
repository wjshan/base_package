# -*- coding: utf-8 -*-
# (C) shan weijia, 2018
# All rights reserved

'''Description '''

__author__ = 'shan weijia <shanweijia@jiaaocap.com>'
__time__ = '2018/12/17 9:24 AM'

from global_reference import HttpError

error_code = {
    200: "请求成功",
    1001: "登录异常,用户名为空",
    1002: "登录异常,密码错误",
    1003: "非法登录,未注册用户",
    4001: "登录凭证异常,超时时间丢失,请重新登录",
    4002: "登录凭证异常,非法的超时时间,请重新登录",
    4003: "登录凭证异常,超时,请重新登录",
    4004: "登录凭证异常,解析错误,请重新登录",
    4005: "登录凭证异常,访问拒绝,请登录",
}


def retrun_error(code):
    message = error_code.get(code, "未知错误")
    raise HttpError(code=code, message=message)
