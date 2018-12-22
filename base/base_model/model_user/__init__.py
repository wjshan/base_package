# -*- coding: utf-8 -*-
# (C) shan weijia, 2018
# All rights reserved

'''Description '''

__author__ = 'shan weijia <shanweijia@jiaaocap.com>'
__time__ = '2018/11/9 3:57 PM'

from ..model_base import TableBase
from global_reference import db


class User(db.Model, TableBase):
    _log_user = False
    name = db.Column(db.String(32), comment="用户名称")
    passwd = db.Column(db.String(32), comment="密码MD5")
    head = db.Column(db.String(64), comment="头像图片地址")

    def __init__(self, name, passwd, head, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.name = name
        self.passwd = passwd
        self.head = head
