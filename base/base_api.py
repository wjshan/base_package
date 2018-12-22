# -*- coding: utf-8 -*-
# (C) shan weijia, 2018
# All rights reserved

'''Description '''

__author__ = 'shan weijia <shanweijia@jiaaocap.com>'
__time__ = '2018/12/22 8:48 PM'
from flask_restful import Api
from global_reference import HttpError
class BaseApi(Api):
    def handle_error(self, e):
        if isinstance(e,HttpError):
            return {"code":e.code,"message":e.message,"data":{}}
        return {"code":500,"message":str(e)}

