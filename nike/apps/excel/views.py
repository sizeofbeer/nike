# -*- coding:utf8  -*-
from flask_restful import Resource
from config import app
from flask import request, send_file
from werkzeug.utils import secure_filename
import os, zipfile, json, uuid
from apps.excel.models import *
from apps.utils import *

''' 标准上传/下载/excel导数据库 '''
class downloadFile(Resource):
    def get(self, id):
        result_path = os.path.join(path, id)
        result_path = os.path.join(result_path, 'Result')
        result_file = os.path.join(result_path, 'result.zip')
        if os.path.exists(result_file):
            os.remove(result_file)
        zipf = zipfile.ZipFile(result_file, 'w', zipfile.ZIP_DEFLATED)
        for _, _, files in os.walk(result_path):
            for file in files:
                if 'result.zip' not in file:
                    zipf.write(os.path.join(result_path, file), arcname=str(file))
        zipf.close()
        return send_file(result_file,
                mimetype = 'zip',
                attachment_filename= 'result.zip',
                as_attachment = True)
class uploadFile(Resource):
    def post(self):
        returnData = {
            'status': 0,
            'msg': '',
            'id': ''
        }
        try:
            task_msg = json.loads(request.form.get('key'))
            # print(task_msg)
            code = task_msg["config"]
            task_id = task_msg['keyID']
            task_name = task_msg['taskname']
            insert_data = []
            insert_data.append([task_id, task_name, code])
            ''' 任务ID创建文件夹 '''
            # print(code, task_id)
            task_path = os.path.join(path, task_id)
            # print(task_path)
            init_task_folder(task_path)
            uploaded_files = request.files.getlist('file')
            # print(uploaded_files)
            for f in uploaded_files:
                if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
                    # fname = secure_filename(f.filename)  # 中文处理异常
                    filefullpath = os.path.join(task_path, f.filename)
                    f.save(filefullpath)  # 保存文件到upload目录
            nike_task = NikeTask()
            task_search = nike_task.query.filter_by(taskid=task_id).first()
            if not task_search:
                db.session.execute(nike_task.__table__.insert(),
                    [{
                        "taskid": data[0], "context": data[1], "service": data[2]
                    } for data in insert_data]
                )
                db.session.commit()
            else:
                returnData['msg'] = "任务id错误, 请重新上传"
                return returnData
            returnData['status'] = 1
            returnData['msg'] = "任务创建完成"
            returnData['id'] = str(task_id)
            return returnData
        except Exception as error:
            returnData['msg'] = str(error)
            return returnData
''' 集成功能写的一些接口 '''
class NikeSomeAmusing(Resource):
    def post(self, id):
        returnData = {
            'status': 0,
            'msg': '',
            'access': '',
            'url': ''
        }
        try:
            nike_task = NikeTask()
            task_search = nike_task.query.filter_by(taskid=id).first()
            if not task_search:
                returnData['msg'] = "task_id not exist"
                returnData['status'] = 2
                return returnData
            if task_search.access == '100':
                returnData['status'] = 1
                returnData['msg'] = 'task is finished'
                returnData['access'] = '100'
                returnData['url'] = app.config['WEB_URL'] + '/Nike_Download/' + id
                return returnData
            if task_search.abnormal != "":
                returnData['status'] = 2
                returnData['msg'] = task_search.abnormal
            else:
                returnData['status'] = 0
                returnData['msg'] = 'the task is working'
                returnData['access'] = task_search.access
            return returnData
        except Exception as error:
            returnData['status'] = 2
            returnData['msg'] = str(error)
            return returnData
from apps.excel.nike_ob_bill import deal_ob_bill
class DealObBill(Resource):
    def post(self, id):
        returnData = {
            'status': 0,
            'msg': ''
        }
        try:
            deal_ob_bill(path, id)
            returnData['status'] = 1
            returnData['msg'] = id
            return returnData
        except Exception as error:
            returnData['msg'] = str(error)
            return returnData
from apps.excel.nike_month_kpi import deal_month_kpi
class DealMonthKpi(Resource):
    def post(self, id):
        returnData = {
            'status': 0,
            'msg': ''
        }
        try:
            deal_month_kpi(path, id)
            returnData['status'] = 1
            returnData['msg'] = id
            return returnData
        except Exception as error:
            returnData['msg'] = str(error)
            return returnData
from apps.excel.system_compares import deal_system_compares
class DealSystemCP(Resource):
    def post(self, id):
        returnData = {
            'status': 0,
            'msg': ''
        }
        try:
            deal_system_compares(path, id)
            returnData['status'] = 1
            returnData['msg'] = id
            return returnData
        except Exception as error:
            returnData['msg'] = str(error)
            return returnData
from apps.excel.same_compares import deal_same_compares
class DealSameCP(Resource):
    def post(self, id):
        returnData = {
            'status': 0,
            'msg': ''
        }
        #if True:
        try:
            deal_same_compares(path, id)
            returnData['status'] = 1
            returnData['msg'] = id
            return returnData
        except Exception as error:
            returnData['msg'] = str(error)
            return returnData