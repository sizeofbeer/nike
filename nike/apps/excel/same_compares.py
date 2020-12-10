from apps.utils import *
from apps.excel.models import *
import warnings, datetime, time, math, re, os
warnings.filterwarnings("ignore")

def deal_same_compares(path, id):
    start = time.time()
    filters = {}
    ac_filters = {}
    '''
    Step1 查询任务状态
        1、任务是否存在
        2、任务是否异常结束
        3、任务是否完成
    '''
    nike_task = NikeTask()
    task = nike_task.query.filter_by(taskid=id).first()
    if task:
        # print(task.taskid, task.context, task.service, task.access, task.abnormal)
        if task.abnormal:
            return
        if task.access == "100":
            return
        '''
        Step2 校验Excel是否符合要求(通过文件名)
        '''
        task_path = os.path.join(path, task.taskid)
        file_list = []
        for _, _, k in os.walk(task_path):
            for c_file in k:
                file_list.append(c_file)
        if len(file_list) != 2:
            filters["abnormal"] = "未提供正确数量的表格"
            res = nike_task.query.filter_by(taskid = task.taskid).update(filters)
            db.session.commit()
            return
        f1_input_file = os.path.join(task_path, file_list[0])
        f2_input_file = os.path.join(task_path, file_list[1])
        '''
        Step3 读取Excel数据
        '''
        f1_file_dic, f1_file_sheets, f1_column_dic = {}, [], {}
        f2_file_dic, f2_file_sheets, f2_column_dic = {}, [], {}
        print("正在读取文件: " + file_list[0])
        f1_file_dic, f1_file_sheets, f1_column_dic = get_info_from_excel_v2(f1_file_dic, f1_file_sheets, f1_column_dic, f1_input_file)
        print("done.")
        print("正在读取文件: " + file_list[1])
        f2_file_dic, f2_file_sheets, f2_column_dic = get_info_from_excel_v2(f2_file_dic, f2_file_sheets, f2_column_dic, f2_input_file)
        print("done.")
        for sheet in f1_file_sheets:
            if sheet not in f2_file_sheets:
                continue
            f1_cp_data = f1_file_dic[sheet]
            f2_cp_data = f2_file_dic[sheet]
            for row in f1_cp_data:
                if row in f2_cp_data:
                    continue
        for sheet in f2_file_sheets:
            if sheet not in f1_file_sheets:
                continue