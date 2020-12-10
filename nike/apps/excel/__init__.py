# -*- coding:utf8  -*-
from apps.excel.views import *
from apps.excel.models import *

def regist_excel(api):
    # 标准上传/下载/excel导数据库
    api.add_resource(uploadFile, '/NikeUpload')
    api.add_resource(downloadFile, '/Nike_Download/<id>')
    # nike集成功能
    # 可修改前端route, 前5个统一接口
    api.add_resource(NikeSomeAmusing, '/Nike_Some_Amusing/<id>')
    api.add_resource(DealObBill, '/Nike_Deal_Ob_Bill/<id>')
    api.add_resource(DealMonthKpi, '/Nike_Deal_Month_Kpi/<id>')
    api.add_resource(DealSystemCP, '/Nike_System_CP/<id>')
    api.add_resource(DealSameCP, '/Nike_Same_CP/<id>')