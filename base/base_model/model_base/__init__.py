# -*- coding: utf-8 -*-
# (C) shan weijia, 2018
# All rights reserved

'''Description 数据库模型基础类'''

__author__ = 'shan weijia <shanweijia@jiaaocap.com>'
__time__ = '2018/11/12 8:40 AM'

from global_reference import db
from sqlalchemy.ext.declarative import AbstractConcreteBase, declared_attr, declarative_base
Base = declarative_base()

class TableBase(AbstractConcreteBase, Base):
    _log_access = True  # 是否添加时间类字段
    _log_user = True  # 是否添加用户字段

    @declared_attr
    def id(cls):
        return db.Column(db.Integer, primary_key=True, autoincrement=True, comment="The primary key of table")

    @declared_attr
    def create_time(cls):
        if cls._log_access:
            return db.Column(db.DateTime, comment="Create on datetime")
        return None

    @declared_attr
    def update_time(cls):
        if cls._log_access:
            return db.Column(db.DateTime, comment="Update on datetime")
        return None

    @declared_attr
    def create_user(cls):
        if cls._log_user:
            return db.Column(db.Integer, db.ForeignKey("user.id"), comment="create by user")
        return None

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @declared_attr
    def __mapper_args__(cls):
        return {'polymorphic_identity': cls.__name__, 'concrete': True} if cls.__name__ != "TableBase" else {}

    def __init__(self, *args, **kwargs):
        self.create_user = kwargs.get("user_id")
