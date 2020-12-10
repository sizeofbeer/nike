from apps.utils import *
from apps.excel.models import *
import warnings, datetime, time, math, re
warnings.filterwarnings("ignore")

def deal_pod_checking(OB_data):
    reason_task = NikeReason()
    doh_task = NikeDtcTime()
    units = 0
    for data in OB_data:
        if not data[5]:
            print("收货单位代码缺失")
            continue
        doh_res = doh_task.query.filter_by(code=data[5]).first()
        if doh_res:
            data[15] = doh_res.requestdoh
            data[16] = doh_res.actualltime
        if data[13]:
            task = reason_task.query.filter_by(reasoncode=data[13]).first()
            if not task:
                print("责任代码错误")
                continue
            data[13] = task.belong
            data[17] = "否"
        if data[5][0] == "8":
            data[0] = "Retail"
        if not data[6]:
            print("箱数缺失")
            data[6] = 0
        data[6] = int(data[6])
        if not data[7]:
            print("件数缺失")
            data[7] = 0
        data[7] = int(data[7])
        units += data[7]
        if data[14]:
            # 实际在途时间 = 实际签收时间 - 发货时间，转换为时间戳计算
            temp_time = format2stamp(data[14]) - format2stamp(data[11])
            if "h" in data[-6]:
                # 空运计算小时，((差值/86400) - 1) * 24
                data[-5] = str(int((((temp_time / 86400) - 1) * 24))) + 'h'
            else:
                # 陆运计算天数，差值/86400
                data[-5] = str(math.floor(temp_time / 86400))
    return units, OB_data
def deal_rt_kpi(RT_data):
    reason_task = NikeReason()
    pick_reason_dic, delivery_reason_dic = {}, {}
    result, details = [], []
    result.append(["考核内容", "标准值", "实际值", "修正值", "实际数", "修正数", "总基数", "备注"])
    orders, units = 0, 0
    for data in RT_data:
        if not data[6]:
            data[6] = 0
        units += int(data[6])
        if data[4] == "嘉善":
            continue
        orders += 1
        if not data[9]:
            continue
        task = reason_task.query.filter_by(reasoncode=data[9]).first()
        data[9] = task.belong
        if "提货" in data[10]:
            data[0] = "提货延迟"
            if data[9] not in pick_reason_dic.keys():
                pick_reason_dic[data[9]] = 0
            pick_reason_dic[data[9]] += 1
        else:
            if data[9] not in delivery_reason_dic.keys():
                delivery_reason_dic[data[9]] = 0
            delivery_reason_dic[data[9]] += 1
        details.append(data)
    
    pick_act, pick_revise, pick_mark = orders, orders, ""
    for i, key in enumerate(pick_reason_dic.keys()):
        pick_act -= pick_reason_dic[key]
        if (i + 1) == len(pick_reason_dic.keys()):
            pick_mark += key + str(pick_reason_dic[key]) + "票。"
        else:
            pick_mark += key + str(pick_reason_dic[key]) + "票，"
    if "承运商原因" in pick_reason_dic.keys():
        pick_revise -= pick_reason_dic["承运商原因"]
    result.append(["提货准时率", "<=2 days", str(round(pick_act / orders * 100, 2)) + "%",
                str(round(pick_revise / orders * 100, 2)) + "%", pick_act, pick_revise, orders, pick_mark])
    
    delivery_act, delivery_revise, delivery_mark = orders, orders, ""
    for i, key in enumerate(delivery_reason_dic.keys()):
        delivery_act -= delivery_reason_dic[key]
        if (i + 1) == len(delivery_reason_dic.keys()):
            delivery_mark += key + str(delivery_reason_dic[key]) + "票。"
        else:
            delivery_mark += key + str(delivery_reason_dic[key]) + "票，"
    if "承运商原因" in delivery_reason_dic.keys():
        delivery_revise -= delivery_reason_dic["承运商原因"]
    result.append(["退货准时率", "FY18 RT LT standard", str(round(delivery_act / orders * 100, 2)) + "%",
                str(round(delivery_revise / orders * 100, 2)) + "%", delivery_act, delivery_revise, orders, delivery_mark])
    result.append([])
    result.append(["退货异常情况明细"])
    result.append(["异常类型","通知提货日期","实际提货日期","退货单号","城市",
                "客户名称","件数","预计退货日期","退货日期","责任归属","异常描述"])
    result += details
    return units, result
def deal_Delay_Details(delay_data):
    unit_carton_dic = {}
    temp, no_repeat_details = [], []
    reason_task = NikeReason()
    for data in delay_data:
        if data[4] not in unit_carton_dic.keys():
            unit_carton_dic[data[4]] = {}
            unit_carton_dic[data[4]]["carton"] = int(data[8])
            unit_carton_dic[data[4]]["unit"] = int(data[9])
            temp.append(data)
        else:
            unit_carton_dic[data[4]]["carton"] += int(data[8])
            unit_carton_dic[data[4]]["unit"] += int(data[9])
    channel_reason = {}
    sum_KA, sum_NSP_Other, sum_NSO, sum_NFS = 0, 0, 0, 0
    for data in temp:
        if not data[0]:
            print("客户代码缺失")
            continue
        if data[0][0] == "8":
            data[0] = "Retail"
        else:
            data[0] = "Normal"
        if data[0] == "Normal":
            if "滔搏" in data[7] or "宝盛" in data[7] or "好孩子" in data[7]:
                data[1] = "KA"
                sum_KA += 1
            else:
                data[1] = "NSP OTHERS"
                sum_NSP_Other += 1
        else:
            if "三里屯" in data[7] or "中关村" in data[7]:
                data[1] = "NSO"
                sum_NSO += 1
            else:
                data[1] = "NFS"
                sum_NFS += 1
        if not data[14]:
            continue
        data[8] = unit_carton_dic[data[4]]["carton"]
        data[9] = unit_carton_dic[data[4]]["unit"]
        mearchObj = re.search(r'CRD要求(\d{4}/\d{1,2}/\d{1,2})', data[17], re.M|re.I)
        if mearchObj:
            data[12] = mearchObj.group(1)
        task = reason_task.query.filter_by(reasoncode=data[14]).first()
        if not task:
            print("责任代码无效")
            continue
        data[15] = task.belong
        data[16] = task.describe
        no_repeat_details.append(data)
        key = data[1] + '_' + data[15]
        if key not in channel_reason.keys():
            channel_reason[key] = 0
        channel_reason[key] += 1
    sum_KC, sum_KN, sum_KV, sum_KW, sum_KF1, sum_KF2, sum_KF3 = 0, 0, 0, 0, 0, 0, 0
    sum_TC, sum_TN, sum_TV, sum_TW, sum_TF1, sum_TF2, sum_TF3 = 0, 0, 0, 0, 0, 0, 0
    sum_OC, sum_ON, sum_OV, sum_OW, sum_OF1, sum_OF2, sum_OF3 = 0, 0, 0, 0, 0, 0, 0
    sum_NC, sum_NN, sum_NV, sum_NW, sum_NF1, sum_NF2, sum_NF3 = 0, 0, 0, 0, 0, 0, 0
    for key_word in channel_reason.keys():
        key_tumple = key_word.split("_")
        key_channel = key_tumple[0]
        key_reason = key_tumple[1]
        if key_channel == "KA":
            if key_reason == "客户原因":
                sum_KC = channel_reason[key_word]
            if key_reason == "CRD原因":
                sum_KN = channel_reason[key_word]
            if key_reason == "承运商原因":
                sum_KV = channel_reason[key_word]
            if key_reason == "仓库原因":
                sum_KW = channel_reason[key_word]
            if key_reason == "天气原因":
                sum_KF1 = channel_reason[key_word]
            if key_reason == "交通原因":
                sum_KF2 = channel_reason[key_word]
            if key_reason == "不可抗力":
                sum_KF3 = channel_reason[key_word]
        elif key_channel == "NSP OTHERS":
            if key_reason == "客户原因":
                sum_TC = channel_reason[key_word]
            if key_reason == "CRD原因":
                sum_TN = channel_reason[key_word]
            if key_reason == "承运商原因":
                sum_TV = channel_reason[key_word]
            if key_reason == "仓库原因":
                sum_TW = channel_reason[key_word]
            if key_reason == "天气原因":
                sum_TF1 = channel_reason[key_word]
            if key_reason == "交通原因":
                sum_TF2 = channel_reason[key_word]
            if key_reason == "不可抗力":
                sum_TF3 = channel_reason[key_word]
        elif key_channel == "NSO":
            if key_reason == "客户原因":
                sum_OC = channel_reason[key_word]
            if key_reason == "CRD原因":
                sum_ON = channel_reason[key_word]
            if key_reason == "承运商原因":
                sum_OV = channel_reason[key_word]
            if key_reason == "仓库原因":
                sum_OW = channel_reason[key_word]
            if key_reason == "天气原因":
                sum_OF1 = channel_reason[key_word]
            if key_reason == "交通原因":
                sum_OF2 = channel_reason[key_word]
            if key_reason == "不可抗力":
                sum_OF3 = channel_reason[key_word]
        elif key_channel == "NFS":
            if key_reason == "客户原因":
                sum_NC = channel_reason[key_word]
            if key_reason == "CRD原因":
                sum_NN = channel_reason[key_word]
            if key_reason == "承运商原因":
                sum_NV = channel_reason[key_word]
            if key_reason == "仓库原因":
                sum_NW = channel_reason[key_word]
            if key_reason == "天气原因":
                sum_NF1 = channel_reason[key_word]
            if key_reason == "交通原因":
                sum_NF2 = channel_reason[key_word]
            if key_reason == "不可抗力":
                sum_NF3 = channel_reason[key_word]
    result = []
    result.append(["Channel","Summary","Customer reason","CRD reason","Vender reason","DC reason",
                    "Weather reason","Traffic reason","Other reason","Total OB orders"])
    result.append(["KA", "Orders", sum_KC, sum_KN, sum_KV, sum_KW, sum_KF1, sum_KF2, sum_KF3, sum_KA])
    result.append(["", "Rate", str(round(sum_KC / sum_KA * 100, 2)) + '%', str(round(sum_KN / sum_KA * 100, 2)) + '%',
                        str(round(sum_KV / sum_KA * 100, 2)) + '%', str(round(sum_KW / sum_KA * 100, 2)) + '%',str(round(sum_KF1 / sum_KA * 100, 2)) + '%',
                        str(round(sum_KF2 / sum_KA * 100, 2)) + '%',str(round(sum_KF3 / sum_KA * 100, 2)) + '%', "100.00%"])
    result.append(["NSP OTHERS", "Orders", sum_TC, sum_TN, sum_TV, sum_TW, sum_TF1, sum_TF2, sum_TF3, sum_NSP_Other])
    result.append(["", "Rate", str(round(sum_TC / sum_NSP_Other * 100, 2)) + '%', str(round(sum_TN / sum_NSP_Other * 100, 2)) + '%',
                        str(round(sum_TV / sum_NSP_Other * 100, 2)) + '%', str(round(sum_TW / sum_NSP_Other * 100, 2)) + '%',str(round(sum_TF1 / sum_NSP_Other * 100, 2)) + '%',
                        str(round(sum_TF2 / sum_NSP_Other * 100, 2)) + '%',str(round(sum_TF3 / sum_NSP_Other * 100, 2)) + '%', "100.00%"])
    result.append(["NSO", "Orders", sum_OC, sum_ON, sum_OV, sum_OW, sum_OF1, sum_OF2, sum_OF3, sum_NSO])
    result.append(["", "Rate", str(round(sum_OC / sum_NSO * 100, 2)) + '%', str(round(sum_ON / sum_NSO * 100, 2)) + '%',
                        str(round(sum_OV / sum_NSO * 100, 2)) + '%', str(round(sum_OW / sum_NSO * 100, 2)) + '%',str(round(sum_OF1 / sum_NSO * 100, 2)) + '%',
                        str(round(sum_OF2 / sum_NSO * 100, 2)) + '%',str(round(sum_OF3 / sum_NSO * 100, 2)) + '%', "100.00%"])
    result.append(["NFS", "Orders", sum_NC, sum_NN, sum_NV, sum_NW, sum_NF1, sum_NF2, sum_NF3, sum_NFS])
    result.append(["", "Rate", str(round(sum_NC / sum_NFS * 100, 2)) + '%', str(round(sum_NN / sum_NFS * 100, 2)) + '%',
                        str(round(sum_NV / sum_NFS * 100, 2)) + '%', str(round(sum_NW / sum_NFS * 100, 2)) + '%',str(round(sum_NF1 / sum_NFS * 100, 2)) + '%',
                        str(round(sum_NF2 / sum_NFS * 100, 2)) + '%',str(round(sum_NF3 / sum_NFS * 100, 2)) + '%', "100.00%"])
    result.append(["DIG", "Orders", 0, 0, 0, 0, 0, 0, 0, 0])
    result.append(["", "Rate", "0.00", "0.00", "0.00", "0.00", "0.00", "0.00", "0.00", "0.00"])
    result.append([])
    result.append(['迟到情况分析'])
    result.append(["类型","渠道","发货日期","发货城市","运单号","省份","城市","客户名称","箱数","件数(units)",
                "在途日期","ETA","CRD","到达日期","责任代码","责任归属","责任说明","具体异常描述","项目（可留空）"])
    result += no_repeat_details
    NSP_sum = sum_KC + sum_TC + sum_KN + sum_TN + sum_KV + sum_TV + sum_KW + sum_TW + sum_KF1 + sum_TF1 + sum_KF2 + sum_TF2 + sum_KF3 + sum_TF3
    DTC_sum = sum_OC + sum_NC + sum_ON + sum_NN + sum_OV + sum_NV + sum_OW + sum_NW + sum_OF1 + sum_NF1 + sum_OF2 + sum_NF2 + sum_OF3 + sum_NF3
    summary_OB = [[sum_KC+sum_TC, sum_KN+sum_TN, sum_KV+sum_TV, sum_KW+sum_TW, sum_KF1+sum_TF1, sum_KF2+sum_TF2, sum_KF3+sum_TF3, NSP_sum],
                [sum_OC+sum_NC, sum_ON+sum_NN, sum_OV+sum_NV, sum_OW+sum_NW, sum_OF1+sum_NF1, sum_OF2+sum_NF2, sum_OF3+sum_NF3, DTC_sum]]
    total_number = [sum_KA + sum_NSP_Other, sum_NSO + sum_NFS]
    return result, summary_OB, total_number
def deal_CRW_CLC_KPI(summary_OB, total_number, OB_unit_total, RT_unit_total):
    result = []
    NSP_act_number = total_number[0] - summary_OB[0][7]
    NSP_up_number = total_number[0] - summary_OB[0][2]
    NSP_act = str(round(NSP_act_number / total_number[0] * 100,2)) + '%'
    NSP_up = str(round(NSP_up_number / total_number[0] * 100,2)) + '%'
    DTC_act_number = total_number[1] - summary_OB[1][7]
    DTC_up_number = total_number[1] - summary_OB[1][2]
    DTC_act = str(round(DTC_act_number / total_number[1] * 100,2)) + '%'
    DTC_up = str(round(DTC_up_number / total_number[1] * 100,2)) + '%'
    remark1 = "共迟到" + str(summary_OB[0][7]) +"票，其中客户原因" + str(summary_OB[0][0]) + "票，CRD原因" + \
        str(summary_OB[0][1]) + "票，承运商原因" +str(summary_OB[0][2]) + "票，仓库原因" +str(summary_OB[0][3]) + "票，天气原因" + \
        str(summary_OB[0][4]) + "票，交通原因" +str(summary_OB[0][5]) + "票，其他原因" +str(summary_OB[0][6]) + "票。"
    remark2 = "共迟到" + str(summary_OB[1][7]) +"票，其中客户原因" + str(summary_OB[1][0]) + "票，CRD原因" + \
        str(summary_OB[1][1]) + "票，承运商原因" +str(summary_OB[1][2]) + "票，仓库原因" +str(summary_OB[1][3]) + "票，天气原因" + \
        str(summary_OB[1][4]) + "票，交通原因" +str(summary_OB[1][5]) + "票，其他原因" +str(summary_OB[1][6]) + "票。"
    result.append(["指标","达标值","实际值","修正值","实际数","修正数","总基数","备注","客户","CRD","承运商","仓库","天气","交通","其他","总计"])
    total_unit = OB_unit_total + RT_unit_total
    total = total_number[0] + total_number[1]
    result.append(["普通客户到货准时率", "99.5%>x>=98.00%", NSP_act, NSP_up, NSP_act_number, NSP_up_number, total_number[0],
                        remark1, summary_OB[0][0], summary_OB[0][1], summary_OB[0][2], summary_OB[0][3], summary_OB[0][4], summary_OB[0][5],
                        summary_OB[0][6], summary_OB[0][7]])
    result.append(["DTC+DOH到货准时率", "99.5%>x>=98.00%", DTC_act, DTC_up, DTC_act_number, DTC_up_number, total_number[1],
                        remark2, summary_OB[1][0], summary_OB[1][1], summary_OB[1][2], summary_OB[1][3], summary_OB[1][4], summary_OB[1][5],
                        summary_OB[1][6], summary_OB[1][7]])
    result.append(["事故次数", "x=0", "", "", "", "", 0, ""])
    result.append(["货物残损率", "0.001%<=x<0.03%", "", "", "", "", total_unit, ""])
    result.append(["回单准时率", "99.50%>x>=98.00%", '100.00%', "100.00%", total, total, total, ""])
    result.append(["定性评价", "3.5>X>=2.4", "", "", "", "", "", ""])
    result.append([""])
    result.append(["指标","CO2减排率/件","年度碳排值","月度碳排放值","运输发货总件数","LNG运输件数","LNG覆盖率",
                        "铁路运输件数","铁路覆盖率","总计减排量","本月最终碳排放值","减排比率","FY20 G/U"])
    result.append(["CO2减排", "10.00%", "201", "", "", "", "", "", "", "", "", "", ""])
    return result

def deal_month_kpi(path, id):
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
        OB_input_file = preChecking_inputFile(task_path, "大仓出货")
        if OB_input_file is None:
            filters["abnormal"] = "未正确提供大仓出货数据"
            res = nike_task.query.filter_by(taskid = task.taskid).update(filters)
            db.session.commit()
            return
        OB_input_file = os.path.join(task_path, OB_input_file)
        RT_input_file = preChecking_inputFile(task_path, "退货运单")
        if RT_input_file is None:
            filters["abnormal"] = "未正确提供退货运单数据"
            res = nike_task.query.filter_by(taskid = task.taskid).update(filters)
            db.session.commit()
            return
        RT_input_file = os.path.join(task_path, RT_input_file)
        '''
        Step3 读取Excel数据
        '''
        OB_file_dic, OB_file_sheets, OB_column_dic = {}, [], {}
        RT_file_dic, RT_file_sheets, RT_column_dic = {}, [], {}
        print("正在读取大仓出货数据")
        OB_file_dic, OB_file_sheets, OB_column_dic = get_info_from_excel_v2(OB_file_dic, OB_file_sheets, OB_column_dic, OB_input_file)
        print("done.")
        print("正在读取退货运单数据")
        RT_file_dic, RT_file_sheets, RT_column_dic = get_info_from_excel_v2(RT_file_dic, RT_file_sheets, RT_column_dic, RT_input_file)
        print("done.")
        OB_origin_data = OB_file_dic[OB_file_sheets[0]]
        RT_origin_data = RT_file_dic[RT_file_sheets[0]]
        '''
        Step4 生成POD Checking
        '''
        OB_alpha_list = ['Normal','C','A','R','X','J','L','M','G','I','K','D','P','AB','S','','','是','O','','','Express','B','T']
        OB_data = final_data_consist(OB_origin_data, OB_alpha_list)
        OB_units, OB_data = deal_pod_checking(OB_data)
        '''
        Step5 生成KPI
        '''
        # RT KPI
        RT_alpha_list = ['退货延迟','H','N','D','K','C','Z','M','Q','V','U']
        RT_data = final_data_consist(RT_origin_data, RT_alpha_list)
        RT_units, RT_KPI_data = deal_rt_kpi(RT_data)
        # Delay Details
        delay_list = ['J','','D','G','A','H','I','X','L','M','O','P','','S','AB','','','T','']
        delay_data = final_data_consist(OB_origin_data, delay_list)
        delay_result, summary_OB, total_number = deal_Delay_Details(delay_data)
        # CRW_CLC_KPI
        summary = deal_CRW_CLC_KPI(summary_OB, total_number, OB_units, RT_units)
        result_path = os.path.join(task_path, "Result")
        result_file1 = os.path.join(result_path, "result_POD_Checking.xlsx")
        result_file2 = os.path.join(result_path, "result_Month_KPI.xlsx")
        POD_Check_header = ["自营店/经销商&个人客户","发货号","总单号","承运商 (包括干线运输商和终端运输商)","客户名称",
                            "收货人代码","箱数","件数","发货城市","目的城市","送货地址","发货日期","预计到货日期","责任归属",
                            "实际到货日期","要求送达时间段","到达时间","是否当天到货","在途时间","实际在途时间","POD预计返回时间",
                            "POD返回方式","货物种类","备注"]
        input_excel(result_file1, [POD_Check_header], [OB_data], ['OB'])
        summary_header = ["Nike项目KPI考核表", "", "", "", "", "", "", "", "出货迟到原因（票数）"]
        delay_header = ["迟到数据汇总（按渠道）"]
        RT_header = ["退货分析"]
        input_excel(result_file2, [summary_header, delay_header, RT_header],
                    [summary, delay_result, RT_KPI_data], ["（CRW+CLC) KPI", "Delay Details", "Return Analysis"])
        # ac_filters["access"] = "100"
        # res = nike_task.query.filter_by(taskid = task.taskid).update(ac_filters)
        # db.session.commit()
    else:
        return
    end = time.time()
    print("耗时: {} min".format((end - start) / 60))