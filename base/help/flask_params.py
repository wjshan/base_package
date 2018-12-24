# -*- coding: utf-8 -*-
# (C) shan weijia, 2018
# All rights reserved

'''Description '''

__author__ = 'shan weijia <shanweijia@jiaaocap.com>'
__time__ = '2018/12/24 1:18 PM'

from flask import request


class ArgumentError(Exception):
    def __init__(self, flag, comment, field):
        '''参数检查错误类 用于传递到error_func 交由 调用方处理此错误
        :param flag: 错误标识 not_fund(参数缺失) type_error(参数类型错误) is_None(不允许为None值)
        :type flag str
        :param comment: 错误描述
        :type comment str
        '''
        self.flag = flag
        self.comment = comment
        self.field = field


class Rule(object):
    def __init__(self, field, rule_funcs, location=("json", "form"), error_func=None, call_back=None, require=False,
                 nullable=True):
        '''

        :param field: 字段名称
        :type field str
        :param rule_funcs: 参数校验方法 校验通过返回 True 反之返回False
        :type rule_funcs [function,]
        :param error_func: 参数校验不通过后的回调方法
        :type error_func function
        :param call_back: 参数校验通过之后的回调方法
        :type call_back: function
        :param require: 是否为必须参数,True field必传 且执行rule_func校验 False 参数非必传 如果不传递field则不会进行rule_func校验
        但仍然会调用 call_back
        :type require: bool
        :param nullable 是否允许为None值
        :type nullable bool
        :param location flask.request 中的域 json,form,values
        :type location (str,)   ("json","values")
        '''
        self.field = field
        self.rule_funcs = rule_funcs
        self.location = location
        self.error_func = error_func
        self.call_back = call_back
        self.require = require
        self.nullable = nullable
        self.not_find = False

    def set_default(self, **kwargs):
        self.error_func = self.error_func or kwargs.get("error_func")
        self.call_back = self.call_back or kwargs.get("call_back")
        self.require = self.require or kwargs.get("require")
        self.nullable = self.nullable or kwargs.get("nullable")

    def _run(self):
        field_value = self.get_field_value()
        if self.require and self.not_find:
            self.error_func(ArgumentError("not_fund", "field{0}缺失".format(self.field), self.field))
            return False, field_value
        if field_value is None and not self.nullable:
            self.error_func(ArgumentError("is_None", "field{0}不允许为None".format(self.field), self.field))
            return False, field_value
        for func in self.rule_funcs:
            if not callable(func):
                continue
            if not func(field_value):
                self.error_func(ArgumentError("type_error", "field{0},检查失败,不允许的规则".format(self.field), self.field))
                return False, field_value
        return True, field_value

    def run(self):
        _ok, field_value = self._run()
        if callable(self.call_back):
            return self.call_back(_ok, field_value)
        return field_value

    def get_field_value(self):
        self.not_find = False
        for scope in self.location:
            if not hasattr(request, scope):
                continue
            local = getattr(request, scope)
            if local is None:
                continue
            if self.field not in local:
                continue
            return local.get(self.field)
        self.not_find = True


class Rules(object):
    def __init__(self, *rules, **kwargs):
        self.rules = rules
        # for rule in self.rules:
        #     rule.set_default(**kwargs)

    def run(self):
        params = {}
        for rule in self.rules:
            params[rule.field] = rule.run()
        return params


def phone(field_value):
    pass


import re


def email(field_value):
    return re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', field_value)


def rule_len(n=-1, m=-1):
    def _len(field_value):
        if n >= 0 and len(field_value) < n:
            return False
        if len(field_value) > m >= 0:
            return False
        return True

    return _len


def type_of(type):
    def _type(field_value):
        return

    return _type
