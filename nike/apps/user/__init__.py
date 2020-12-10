# -*- coding:utf8  -*-
from apps.user.views import *
from apps.user.models import *

def regist_user(api):
    # 用户登录/管理
    api.add_resource(NikeLogin, '/Nike_Login')
    api.add_resource(CheckLogin, '/Check_Login')
    api.add_resource(Insert_User, '/Nike_Insert_User')
    api.add_resource(Search_User, '/Nike_Search_User')
    api.add_resource(Delete_User, '/Nike_Delete_User')
    api.add_resource(Update_User, '/Nike_Update_User')