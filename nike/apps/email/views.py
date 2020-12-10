# -*- coding:utf8  -*-
from flask_restful import Resource
from flask import request
import os, time, uuid
from apps.email.models import *
from apps.utils import *

from sqlalchemy.orm import class_mapper
class UploadEmail(Resource):
    def post(self):
        returnData = {
            'status': 0,
            'msg': ''
        }
        #if True:
        try:
            excel_id = uuid.uuid4()
            excel_path = os.path.join(tmp_path, "{}.xlsx".format(excel_id))
            uploaded_files = request.files.getlist('file')
            for f in uploaded_files:
                if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
                    f.save(excel_path)  # 保存文件到upload目录
                    break
            input_file_dic, input_file_sheets, file_column_dic = {}, [], {}
            input_file_dic, input_file_sheets, file_column_dic = get_info_from_excel_v1(input_file_dic, input_file_sheets, file_column_dic, excel_path)
            input_data = input_file_dic[input_file_sheets[0]]
            nike_data = NikeData()
            sql = "replace into nike_data values "
            for i, row in enumerate(input_data):
                if i == len(input_data) - 1:
                    sql += "{}".format(tuple(row))
                else:
                    sql += "{}".format(tuple(row)) + ','
            db.session.execute(sql)
            db.session.commit()
            today = datetime.datetime.today().strftime('%Y/%m/%d')
            est_datas = nike_data.query.filter_by(gi_date = today).all()
            target_datas = []
            if est_datas:
                for i in range(len(est_datas)):
                    est_row = [getattr(est_datas[i], c.key) for c in class_mapper(est_datas[i].__class__).columns]
                    target_datas.append(est_row)
            out_path = os.path.join(path, "Est_Report.xlsx")
            header = ["总单号","BU","发货单号","发货时间","出发城市","目的城市","客户代码","卸货地址","箱数","件数",
                    "陆运/铁运/空运","在途时间","预计到达时间","状态","承运商(包括干线商和终端运输商)","实际签收时间",
                    "跟踪备注","托运单备注","第1天","第2天","第3天","第4天","第5天","第6天","第7天","第8天","第9天",
                    "第10天","第11天","第12天","第13天","第14天","第15天","Abnormal Issue 异常信息","客户简称",
                    "客户名称","收货人","联系方式","联系人手机","是否预报","预报人","客户类型"]
            input_excel(out_path, [header], [target_datas], ['Sheet1'])
            send_tag = send_email(out_path)
            print('邮件发送: ',send_tag)
            returnData['status'] = 1
            returnData['msg'] = "数据上传完成"
            return returnData
        except Exception as error:
            returnData['msg'] = str(error)
            return returnData