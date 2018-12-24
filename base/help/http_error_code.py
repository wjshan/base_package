# -*- coding: utf-8 -*-
# (C) shan weijia, 2018
# All rights reserved

'''Description '''

__author__ = 'shan weijia <shanweijia@jiaaocap.com>'
__time__ = '2018/12/17 9:24 AM'

from global_reference import HttpError

error_code = {
    200: "请求成功",
    405: "未定义的路由请求方式",

    1001: "登录异常,用户名为空",
    1002: "登录异常,密码错误",
    1003: "您还没有注册，请先登记一下吧!",
    1004: "您的账号尚未激活,请联系管理员",

    2001: "参数不完整,缺少必填参数",
    2002: "参数不合法,检测失败",
    2003: "参数不允许为空",

    3001: "两次输入的密码不一致",
    3002: "用户名已存在",
    3003: "邮箱已存在",
    3004: "账号已存在",

    4001: "登录凭证异常,超时时间丢失,请重新登录",
    4002: "登录凭证异常,非法的超时时间,请重新登录",
    4003: "登录凭证异常,超时,请重新登录",
    4004: "登录凭证异常,解析错误,请重新登录",
    4005: "登录凭证异常,访问拒绝,请登录",
}


def retrun_error(code, message=None):
    message = message or error_code.get(code, "未知错误")
    raise HttpError(code=code, message=message)
