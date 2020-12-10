# -*- coding:utf8  -*-
from flask_restful import Resource
from flask import request
import os, json, uuid
from apps.kpi.models import *
from apps.utils import *

''' 一些KPI图表 '''
from apps.kpi.actions import kpi_show
class KPIVisualize(Resource):
    def post(self):
        returnData = {
            'status': 0,
            'data': {}
        }
        #if True:
        try:
            key_dict = request.json
            # print(key_dict)
            returnData['data'] = kpi_show()
            returnData['status'] = 1
            return returnData
        except Exception as error:
            return returnData
from apps.kpi.actions import rank_show
class RANKVisualize(Resource):
    def post(self):
        returnData = {
            'status': 0,
            'data': []
        }
        #if True:
        try:
            key_dict = request.json
            # print(key_dict)
            returnData['data'] = rank_show()
            returnData['status'] = 1
            return returnData
        except Exception as error:
            return returnData
from apps.kpi.actions import kpi_merits
class KPIScore(Resource):
    def post(self):
        returnData = {
            'title': '',
            'status': 0,
            'Positive': [],
            'msg': ''
        }
        try:
            key_dict = request.json
            # print(key_dict)
            month = key_dict['ShowNumber']
            returnData['Positive'] = kpi_merits(str(int(month)))
            returnData['status'] = 1
            if len(str(month)) == 1:
                month = '0' + str(month)
            returnData['title'] = "2020年" + str(month) + "月绩效排名"
            returnData['msg'] = "数据展示完成"
            return returnData
        except Exception as error:
            return returnData
''' 中台数据录入 '''
from apps.kpi.actions import CenterKPI_to_DB
class CenterUpDatabase(Resource):
    def post(self):
        returnData = {
            'status': 0,
            'msg': ''
        }
        #if True:
        try:
            xls_id = uuid.uuid4()
            xls_path = os.path.join(tmp_path, "{}.xlsx".format(xls_id))
            try:
                f = request.files['file']
                if not f:
                    returnData['msg'] = "文件未上传"
                    return returnData
                f.save(xls_path)
            except Exception:
                returnData['msg'] = "文件上传失败"
                return returnData
            CenterKPI_to_DB(xls_path)
            returnData['status'] = 1
            returnData['msg'] = "录入成功"
            return returnData
        except Exception as error:
            returnData['msg'] = str(error)
            return returnData
from apps.kpi.actions import TransportKPI_to_DB
class TransportUpDatabase(Resource):
    def post(self):
        returnData = {
            'status': 0,
            'msg': ''
        }
        #if True:
        try:
            xls_id = uuid.uuid4()
            xls_path = os.path.join(tmp_path, "{}.xlsx".format(xls_id))
            try:
                f = request.files['file']
                if not f:
                    returnData['msg'] = "文件未上传"
                    return returnData
                f.save(xls_path)
            except Exception:
                returnData['msg'] = "文件上传失败"
                return returnData
            TransportKPI_to_DB(xls_path)
            returnData['status'] = 1
            returnData['msg'] = "录入成功"
            return returnData
        except Exception as error:
            returnData['msg'] = str(error)
            return returnData
from apps.kpi.actions import show_month_transport
class TransportShowKPI(Resource):
    def post(self):
        returnData = {
            'status': 0,
            'data': {}
        }
        #if True:
        try:
            key_dict = request.json
            # print(key_dict)
            returnData['data'] = show_month_transport()
            returnData['status'] = 1
            return returnData
        except Exception as error:
            return returnData
