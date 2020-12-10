from apps.utils import *
from apps.excel.models import *
import warnings, datetime, time, math, re
warnings.filterwarnings("ignore")

def code2BU(string):
    if string == "20":
        string = "FW"
    elif string == "10":
        string = "APP"
    elif string == "30":
        string = "EQ"
    else:
        pass
    return string
def deal_system_compares(path, id):
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
        WCI_input_file, TMS_input_file = "", ""
        if task.service == "OB":
            '''
            Step2 校验Excel是否符合要求(通过文件名)
            '''
            task_path = os.path.join(path, task.taskid)
            WCI_input_file = preChecking_inputFile(task_path, "Tracking")
            if WCI_input_file is None:
                filters["abnormal"] = "未正确提供Tracking数据"
                res = nike_task.query.filter_by(taskid = task.taskid).update(filters)
                db.session.commit()
                return
            WCI_input_file = os.path.join(task_path, WCI_input_file)
            TMS_input_file = preChecking_inputFile(task_path, "大仓出货")
            if TMS_input_file is None:
                filters["abnormal"] = "未正确提供大仓出货数据"
                res = nike_task.query.filter_by(taskid = task.taskid).update(filters)
                db.session.commit()
                return
            TMS_input_file = os.path.join(task_path, TMS_input_file)
        elif task.service == "RT":
            '''
            Step2 校验Excel是否符合要求(通过文件名)
            '''
            task_path = os.path.join(path, task.taskid)
            WCI_input_file = preChecking_inputFile(task_path, "RTShipOrder")
            if WCI_input_file is None:
                filters["abnormal"] = "未正确提供RTShipOrder数据"
                res = nike_task.query.filter_by(taskid = task.taskid).update(filters)
                db.session.commit()
                return
            WCI_input_file = os.path.join(task_path, WCI_input_file)
            TMS_input_file = preChecking_inputFile(task_path, "退货运单")
            if TMS_input_file is None:
                filters["abnormal"] = "未正确提供退货运单数据"
                res = nike_task.query.filter_by(taskid = task.taskid).update(filters)
                db.session.commit()
                return
            TMS_input_file = os.path.join(task_path, TMS_input_file)
        # elif task.service == "ST":
        #     '''
        #     Step2 校验Excel是否符合要求(通过文件名)
        #     '''
        #     task_path = os.path.join(path, task.taskid)
        #     WCI_input_file = preChecking_inputFile(task_path, "大仓出货")
        #     if WCI_input_file is None:
        #         filters["abnormal"] = "未正确提供大仓出货数据"
        #         res = nike_task.query.filter_by(taskid = task.taskid).update(filters)
        #         db.session.commit()
        #         return
        #     WCI_input_file = os.path.join(task_path, WCI_input_file)
        #     TMS_input_file = preChecking_inputFile(task_path, "退货运单")
        #     if TMS_input_file is None:
        #         filters["abnormal"] = "未正确提供退货运单数据"
        #         res = nike_task.query.filter_by(taskid = task.taskid).update(filters)
        #         db.session.commit()
        #         return
        #     TMS_input_file = os.path.join(task_path, TMS_input_file)
        
        '''
        Step3 读取Excel数据
        '''
        WCI_file_dic, WCI_file_sheets, WCI_column_dic = {}, [], {}
        TMS_file_dic, TMS_file_sheets, TMS_column_dic = {}, [], {}
        print("正在读取WCI数据")
        WCI_file_dic, WCI_file_sheets, WCI_column_dic = get_info_from_excel_v2(WCI_file_dic, WCI_file_sheets, WCI_column_dic, WCI_input_file)
        print("done.")
        print("正在读取TMS数据")
        TMS_file_dic, TMS_file_sheets, TMS_column_dic = get_info_from_excel_v2(TMS_file_dic, TMS_file_sheets, TMS_column_dic, TMS_input_file)
        print("done.")
        WCI_origin_data = WCI_file_dic[WCI_file_sheets[0]]
        TMS_origin_data = TMS_file_dic[TMS_file_sheets[0]]
        WCI_dic, TMS_dic = {}, {}
        if task.service == "OB":
            WCI_list = ['B','C','D','F','H','K','L','N','Q','T','U','AA']
            WCI_data = final_data_consist(WCI_origin_data, WCI_list)
            for data in WCI_data:
                if "总单号" in data:
                    continue
                data[0] = data[0].upper()
                data[1] = data[1].upper()
                data[2] = stamp_format(data[2])
                if data[4]:
                    data[4] = str(int(data[4]))
                if data[7]:
                    data[7] = code2BU(data[7])
                data[8] = stamp_format(data[8])
                data[9] = stamp_format(data[9])
                if data[1] not in WCI_dic.keys():
                    WCI_dic[data[1]] = data
                else:
                    print(data[1] + ": 发货号已存在WCI")
            TMS_list = ['A','C','D','I','J','L','M','B','P','S','T','AB']
            TMS_data = final_data_consist(TMS_origin_data, TMS_list)
            for data in TMS_data:
                data[0] = data[0].upper()
                data[1] = data[1].upper()
                data[2] = stamp_format(data[2])
                if data[4]:
                    data[4] = str(int(data[4]))
                data[8] = stamp_format(data[8])
                data[9] = stamp_format(data[9])
                if data[1] not in TMS_dic.keys():
                    TMS_dic[data[1]] = data
                else:
                    print(data[1] + ": 发货号已存在TMS")
        elif task.service == "RT":
            WCI_list = ['A','D','H','I','N','Q','R','U','V']
            WCI_data = final_data_consist(WCI_origin_data, WCI_list)
            for data in WCI_data:
                if "客户代码" in data:
                    continue
                data[1] = data[1].upper()
                if data[0]:
                    data[0] = str(int(data[0]))
                data[5] = stamp_format(data[5])
                data[6] = stamp_format(data[6])
                if data[1] not in WCI_dic.keys():
                    WCI_dic[data[1]] = data
                else:
                    print(data[1] + ": 发货号已存在WCI")
            TMS_list = ['A','D','Z','AA','K','N','Q','U','V']
            TMS_data = final_data_consist(TMS_origin_data, TMS_list)
            for data in TMS_data:
                data[1] = data[1].upper()
                if data[0]:
                    data[0] = str(int(data[0]))
                data[5] = stamp_format(data[5])
                data[6] = stamp_format(data[6])
                if data[1] not in TMS_dic.keys():
                    TMS_dic[data[1]] = data
                else:
                    print(data[1] + ": 发货号已存在TMS")
        # elif task.service == "ST":
        #     WCI_list = ['J','','D','G','A','H','I','X','L','M','O','P','','S','AB','','','T','']
        #     WCI_data = final_data_consist(WCI_origin_data, WCI_list)
        #     TMS_list = ['J','','D','G','A','H','I','X','L','M','O','P','','S','AB','','','T','']
        #     TMS_data = final_data_consist(TMS_origin_data, TMS_list)
        surplus_wci, surplus_tms = [], []
        differ_data, differ_local = [], []
        for wci_key in WCI_dic.keys():
            if wci_key in TMS_dic.keys():
                if WCI_dic[wci_key] != TMS_dic[wci_key]:
                    differ_data.append(["WCI"] + WCI_dic[wci_key])
                    differ_data.append(["TMS"] + TMS_dic[wci_key])
                    temp = []
                    for i in range(len(WCI_dic[wci_key])):
                        if WCI_dic[wci_key][i] != TMS_dic[wci_key][i]:
                            temp.append(i + 1)
                    differ_local.append(temp)
            else:
                print("WCI存在差异单号")
                surplus_wci.append(["WCI"] + WCI_dic[wci_key])
        for tms_key in TMS_dic.keys():
            if tms_key not in WCI_dic.keys():
                print("TMS存在差异单号")
                surplus_tms.append(["TMS"] + WCI_dic[tms_key])
        result_path = os.path.join(task_path, "Result")
        result_file = os.path.join(result_path, "Result_System_Compares.xlsx")
        header = []
        if task.service == "OB":
            header = ["数据源","总单号","发货号","发货日期","目的城市","收货人代码","箱数","件数",
                "产品类型","预计到货日期","实际到货日期","备注","责任代码"]
        elif task.service == "RT":
            header = ["数据源","客户代码","退货编号","实际提货件数","实际提货箱数",
                "提货城市","提货时间","仓库实际收货时间","异常备注","责任归属"]
        differ_input_excel(result_file, [header, header, header], [differ_data, surplus_wci, surplus_tms],
                                    [differ_local, [], []], ["系统对比差异", "WCI多出单号", "TMS多出单号"])
        # ac_filters["access"] = "100"
        # res = nike_task.query.filter_by(taskid = task.taskid).update(ac_filters)
        # db.session.commit()
    else:
        return
    end = time.time()
    print("耗时: {} min".format((end - start) / 60))