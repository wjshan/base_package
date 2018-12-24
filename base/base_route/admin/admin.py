# -*- coding: utf-8 -*-
# (C) shan weijia, 2018
# All rights reserved

'''Description '''

__author__ = 'shan weijia <shanweijia@jiaaocap.com>'
__time__ = '2018/12/24 9:12 AM'

from . import admin_api
from flask_restful import Resource, request
from flask_migrate import Migrate, migrate, init, upgrade
from global_reference import db, app
import os
from base.help.token import TokenAuth

Migrate(app, db)


@admin_api.resource("/dbUpgrade")
class AdminDbUpgrade(Resource):
    @TokenAuth(token_func=lambda x: request.args.get(x))
    def get(self, payload):
        if not os.path.exists("db_back"):
            init(directory="db_back")
        migrate(directory="db_back")
        upgrade(directory="db_back")
        return "database {} update success!".format(db.engine.url.database)
