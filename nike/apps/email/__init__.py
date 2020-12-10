# -*- coding:utf8  -*-
from apps.email.views import *
from apps.email.models import *

def regist_email(api):
    # 标准上传/下载/excel导数据库
    api.add_resource(UploadEmail, '/email_upload')