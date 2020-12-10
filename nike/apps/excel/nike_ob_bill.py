from apps.utils import *
from apps.excel.models import *
import warnings, datetime, time
warnings.filterwarnings("ignore")

def get_order_profile(data_dic, order_type, result_data):
    if order_type == "空运":
        pc_task = NikeAir()
        result_data = get_air_price(pc_task, data_dic, result_data) 
    elif order_type == "退货":
        pc_task = NikeRoad()
        result_data = get_return_price(pc_task, data_dic, order_type, result_data)
    elif order_type == "廊坊":
        pc_task = NikeBzbj()
        pc_task_dtc = NikeBzbjDtc()
        result_data = get_road_price(pc_task, pc_task_dtc, data_dic, order_type, result_data)
    else:
        pc_task = NikeRoad()
        pc_task_dtc = NikeDtc()
        result_data = get_road_price(pc_task, pc_task_dtc, data_dic, order_type, result_data)
    return result_data
def get_air_price(pc_task, data_dic, result_data):
    for key in data_dic.keys():
        search_city = key.split("-")[1]
        task = pc_task.query.filter_by(city=search_city).first()
        if not task:
            print("新增空运城市: " + search_city)
            continue
        if data_dic[key][1] <= 100:
            for data in data_dic[key][0]:
                data[29] = "x<=100kg"
                data[12] = float(task.std1)
                data[14] = float(round_float(data[12] * data[13], 4))
                data[20] = data[17] = float(round_float(data[14] * 0.98, 4))
        elif data_dic[key][1] <= 500:
            for data in data_dic[key][0]:
                data[29] = "100<x<=500kg"
                data[12] = float(task.std2)
                data[14] = float(round_float(data[12] * data[13], 4))
                data[20] = data[17] = float(round_float(data[14] * 0.98, 4))
        else:
            for data in data_dic[key][0]:
                data[29] = "x>500kg"
                data[12] = float(task.std3)
                data[14] = float(round_float(data[12] * data[13], 4))
                data[20] = data[17] = float(round_float(data[14] * 0.98, 4))
        result_data += data_dic[key][0]
    return result_data
def get_return_price(pc_task, data_dic, order_type, result_data):
    for key in data_dic.keys():
        search_city = key.split("-")[1]
        task = pc_task.query.filter_by(city=search_city).first()
        if not task:
            print("新增" + order_type + "城市: " + search_city)
            continue
        if data_dic[key][1] <= 1:
            for data in data_dic[key][0]:
                data[29] = "X《1CBM"
                data[12] = float(task.std1)
                data[14] = float(round_float(data[12] * data[9], 4))
                data[20] = data[17] = float(round_float(data[14] * 0.98, 4))
        elif data_dic[key][1] <= 10:
            for data in data_dic[key][0]:
                data[29] = "1CBM<X《10CBM"
                data[12] = float(task.std2)
                data[14] = float(round_float(data[12] * data[9], 4))
                data[20] = data[17] = float(round_float(data[14] * 0.98, 4))
        elif data_dic[key][1] <= 40:
            for data in data_dic[key][0]:
                data[29] = "10CBM<X《40CBM"
                data[12] = float(task.std3)
                data[14] = float(round_float(data[12] * data[9], 4))
                data[20] = data[17] = float(round_float(data[14] * 0.98, 4))
        elif data_dic[key][1] <= 80:
            for data in data_dic[key][0]:
                data[29] = "40CBM<X《80CBM"
                data[12] = float(task.std4)
                data[14] = float(round_float(data[12] * data[9], 4))
                data[20] = data[17] = float(round_float(data[14] * 0.98, 4))
        else:
            for data in data_dic[key][0]:
                data[29] = "X>80CBM"
                data[12] = float(task.std5)
                data[14] = float(round_float(data[12] * data[9], 4))
                data[20] = data[17] = float(round_float(data[14] * 0.98, 4))
        result_data += data_dic[key][0]
    return result_data
def get_road_price(pc_task, pc_task_dtc, data_dic, order_type, result_data):
    csc_task = NikeWarehouse()
    for key in data_dic.keys():
        search_city = key.split("-")[1]
        if data_dic[key][1] <= 1:
            for data in data_dic[key][0]:
                data[29] = "X《1CBM"
                res = csc_task.query.filter_by(shipto=data[3]).first()
                if (not res) and (data[-5] == "Retail"):
                    task = pc_task_dtc.query.filter_by(city=search_city).first()
                    if not task:
                        print("新增" + order_type + "DTC城市: " + search_city)
                        continue
                    data[12] = float(task.std1)
                    data[14] = float(round_float(data[12] * data[9], 4))
                    data[20] = data[17] = float(round_float(data[14] * 0.98, 4))
                else:
                    task = pc_task.query.filter_by(city=search_city).first()
                    if not task:
                        print("新增" + order_type + "城市: " + search_city)
                        continue
                    data[12] = float(task.std1)
                    data[14] = float(round_float(data[12] * data[9], 4))
                    data[20] = data[17] = float(round_float(data[14] * 0.98, 4))
        elif data_dic[key][1] <= 10:
            for data in data_dic[key][0]:
                data[29] = "1CBM<X《10CBM"
                res = csc_task.query.filter_by(shipto=data[3]).first()
                if (not res) and (data[-5] == "Retail"):
                    task = pc_task_dtc.query.filter_by(city=search_city).first()
                    if not task:
                        print("新增" + order_type + "DTC城市: " + search_city)
                        continue
                    data[12] = float(task.std2)
                    data[14] = float(round_float(data[12] * data[9], 4))
                    data[20] = data[17] = float(round_float(data[14] * 0.98, 4))
                else:
                    task = pc_task.query.filter_by(city=search_city).first()
                    if not task:
                        print("新增" + order_type + "城市: " + search_city)
                        continue
                    data[12] = float(task.std2)
                    data[14] = float(round_float(data[12] * data[9], 4))
                    data[20] = data[17] = float(round_float(data[14] * 0.98, 4))
        elif data_dic[key][1] <= 40:
            for data in data_dic[key][0]:
                data[29] = "10CBM<X《40CBM"
                res = csc_task.query.filter_by(shipto=data[3]).first()
                if (not res) and (data[-5] == "Retail"):
                    task = pc_task_dtc.query.filter_by(city=search_city).first()
                    if not task:
                        print("新增" + order_type + "DTC城市: " + search_city)
                        continue
                    data[12] = float(task.std3)
                    data[14] = float(round_float(data[12] * data[9], 4))
                    data[20] = data[17] = float(round_float(data[14] * 0.98, 4))
                else:
                    task = pc_task.query.filter_by(city=search_city).first()
                    if not task:
                        print("新增" + order_type + "城市: " + search_city)
                        continue
                    data[12] = float(task.std3)
                    data[14] = float(round_float(data[12] * data[9], 4))
                    data[20] = data[17] = float(round_float(data[14] * 0.98, 4))
        elif data_dic[key][1] <= 80:
            for data in data_dic[key][0]:
                data[29] = "40CBM<X《80CBM"
                res = csc_task.query.filter_by(shipto=data[3]).first()
                if (not res) and (data[-5] == "Retail"):
                    task = pc_task_dtc.query.filter_by(city=search_city).first()
                    if not task:
                        print("新增" + order_type + "DTC城市: " + search_city)
                        continue
                    data[12] = float(task.std4)
                    data[14] = float(round_float(data[12] * data[9], 4))
                    data[20] = data[17] = float(round_float(data[14] * 0.98, 4))
                else:
                    task = pc_task.query.filter_by(city=search_city).first()
                    if not task:
                        print("新增" + order_type + "城市: " + search_city)
                        continue
                    data[12] = float(task.std4)
                    data[14] = float(round_float(data[12] * data[9], 4))
                    data[20] = data[17] = float(round_float(data[14] * 0.98, 4))
        else:
            for data in data_dic[key][0]:
                data[29] = "X>80CBM"
                res = csc_task.query.filter_by(shipto=data[3]).first()
                if (not res) and (data[-5] == "Retail"):
                    task = pc_task_dtc.query.filter_by(city=search_city).first()
                    if not task:
                        print("新增" + order_type + "DTC城市: " + search_city)
                        continue
                    data[12] = float(task.std5)
                    data[14] = float(round_float(data[12] * data[9], 4))
                    data[20] = data[17] = float(round_float(data[14] * 0.98, 4))
                else:
                    task = pc_task.query.filter_by(city=search_city).first()
                    if not task:
                        print("新增" + order_type + "城市: " + search_city)
                        continue
                    data[12] = float(task.std5)
                    data[14] = float(round_float(data[12] * data[9], 4))
                    data[20] = data[17] = float(round_float(data[14] * 0.98, 4))
        result_data += data_dic[key][0]
    return result_data
def deal_ob_bill(path, id):
    start = time.time()
    ac_filters = {}
    filters = {}
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
        Step4 填充账单中非金额类数据(收货单位类型除外)
        '''
        OB_alpha_list = ['C','E','','J','','H','I','K','X','','L','M','','','','-2.00%','','','','','','R','Runbow','N','D','B','Normal','','','','']
        RT_alpha_list = ['D','K','AF','A','','','L','','C','','AA','Z','','','','-2.00%','','','','','','I','Runbow','公路','N','AG','Normal','','','','']
        OB_data = final_data_consist(OB_origin_data, OB_alpha_list)
        RT_data = final_data_consist(RT_origin_data, RT_alpha_list)
        dc_task = NikeDc()
        '''
        用于计算同天同城体积/重量
        数据类型:
        {"day1-city1": [[], 0], "day2-city2": [[], 0]}
        '''
        air_dic, return_dic, bzbj_dic, road_dic = {}, {}, {}, {}
        for data in OB_data:
            if len(data[-7]) < 10:
                print("实际发货时间错误: " + data[-7])
                continue
            if not data[3]:
                print("收货单位代码缺失")
                continue
            if data[3][0] == "8":
                data[-5] = "Retail"
            data[-7] = data[-7].replace("-","/")[:10]
            if not data[10]:
                print("箱数缺失")
                data[10] = 0
            data[10] = int(data[10])
            data[9] = float(round_float(data[10] / 11, 4))
            data[13] = float(round_float(data[10] * 1000 / 66, 4))
            if not data[11]:
                print("件数缺失")
                data[11] = 0
            data[11] = int(data[11])
            task = dc_task.query.filter_by(name=data[1]).first()
            if not task:
                print("请新增" + data[1] + "仓库信息")
                continue
            data[2] = task.address
            day_city = data[-7] + "-" + data[6]
            if "空运" in data[-8]:
                if day_city not in air_dic.keys():
                    air_dic[day_city] = [[], 0]
                air_dic[day_city][0].append(data)
                air_dic[day_city][1] += data[13]
            elif "公路" in data[-8]:
                if "廊坊" in data[1]:
                    if day_city not in bzbj_dic.keys():
                        bzbj_dic[day_city] = [[], 0]
                    bzbj_dic[day_city][0].append(data)
                    bzbj_dic[day_city][1] += data[9]
                    continue
                if day_city not in road_dic.keys():
                    road_dic[day_city] = [[], 0]
                road_dic[day_city][0].append(data)
                road_dic[day_city][1] += data[9]
            else:
                print(data[0] + "采用非空运/公路/铁路")
                continue
        for data in RT_data:
            if len(data[-7]) < 10:
                print("实际发货时间错误: " + data[-7])
                continue
            if not data[3]:
                print("收货单位代码缺失")
                continue
            if data[3][0] == "8":
                data[-5] = "Retail"
            data[-7] = data[-7].replace("-","/")[:10]
            if not data[10]:
                print("箱数缺失")
                data[10] = 0
            data[10] = int(data[10])
            data[9] = float(round_float(data[10] / 11, 4))
            data[13] = float(round_float(data[10] * 1000 / 66, 4))
            if not data[11]:
                print("件数缺失")
                data[11] = 0
            data[11] = int(data[11])
            task = dc_task.query.filter_by(name=data[6]).first()
            if not task:
                print("请新增" + data[6] + "仓库信息")
                continue
            if "上海" in data[6]:
                data[5] = "上海市"
            elif "廊坊" in data[6]:
                data[5] = "河北省"
            else:
                data[5] = "江苏省"
            data[7] = task.address
            day_city = data[-7] + "-" + data[1]
            if day_city not in return_dic.keys():
                return_dic[day_city] = [[], 0]
            return_dic[day_city][0].append(data)
            return_dic[day_city][1] += data[9]
        # print(road_dic["2020/10/02北京"][0], road_dic["2020/10/02北京"][1])
        # print(return_dic["2020/10/23湖州"][0], return_dic["2020/10/23湖州"][1])
        '''
        Step5 计算账单中金额类数据以及补充收货单位类型
        '''
        result_data = []
        result_data = get_order_profile(air_dic, "空运", result_data)
        result_data = get_order_profile(return_dic, "退货", result_data)
        result_data = get_order_profile(bzbj_dic, "廊坊", result_data)
        result_data = get_order_profile(road_dic, "正向公路", result_data)
        '''
        Step6 匹配收货单位类型
        '''
        consignee_task = NikeIndiv()
        for data in result_data:
            if not data[3]:
                continue
            task = consignee_task.query.filter_by(shipto=data[3]).first()
            if not task:
                if data[3][0] == "0":
                    data[4] = "Category"
                    if data[14] < 720.7207:
                        data[14] = 720.7207
                        data[20] = data[17] = float(round_float(data[14] * 0.98, 4))
                elif data[5] == "上海市" or data[5] == "江苏省":
                    if data[3][0] == "8":
                        data[4] = "Retail Return"
                    else:
                        data[4] = "Sales Return"
                else:
                    if data[3][0] == "8":
                        data[4] = "Retail Sales"
                    else:
                        data[4] = "Sales"
                continue
            data[4] = task.department
        '''
        Step7 输出结果文件
        '''
        result_path = os.path.join(task_path, "Result")
        result_file = os.path.join(result_path, "Result_OB_Bill.xlsx")
        header = ["发货单号","装货城市","装货详细地址","收货单位代码","收货单位类型","卸货地址省","卸货地址市","详细卸货地址","客户名称",
                 "体积(cbm)","数量(箱)","数量(件)","成本单价/cbm","重量(千克)","成本","燃油附加费","CLC提货补贴","费用","额外费用",
                 "增值税","总收入","运输公司","耐克物流供应商","空运/公路/海运/铁路","实际发货时间","产品类型(鞋/服装/配件)",
                 "普通客户/耐克自营店","备注","城市等级","订单类型","碳排放(千克)"]
        input_excel(result_file, [header], [result_data], ['Sheet1'])
        # ac_filters["access"] = "100"
        # res = nike_task.query.filter_by(taskid = task.taskid).update(ac_filters)
        # db.session.commit()
    else:
        return
    end = time.time()
    print("耗时: {} min".format((end - start) / 60))