# -*- coding:utf8  -*-
from apps.ocr.views import *
from apps.ocr.models import *

def regist_ocr(api):
    # 一些ocr功能
    api.add_resource(Hilti_Upload, '/hilti_upload') # 上传jpg文件
    api.add_resource(Warehouse_Ocr_Rename, '/warehouse_rename') # 上传jpg文件