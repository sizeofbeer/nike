from os.path import dirname, abspath
import openpyxl, os
from apps.kpi.models import *
from apps.utils import *
path = dirname(abspath(__file__))
source_path = os.path.join(path, "sources")

''' 读取Excel文件数据 '''
def get_info_from_excel2(input_file_dic, input_file_sheets, file_column_dic, input_file):
    xl = openpyxl.load_workbook(input_file, data_only=True)
    xlsx_sheet_names = xl.sheetnames
    for sheet_name in xlsx_sheet_names:
        if sheet_name != '总数据表':
            continue
        table = xl[sheet_name]
        # list [Sheet1, Sheet2]
        input_file_sheets.append(sheet_name)
        # dict {Sheet1: [[1][2][3]], Sheet2: [[1][2][3]]}
        input_file_dic[sheet_name] = []
        # dict {Sheet1: [[0]], Sheet2: [[0]]}
        file_column_dic[sheet_name] = []
        max_row = table.max_row
        max_column = table.max_column
        # 本函数中第一行不为空
        # print(input_file, max_column)
        colume_info = []
        # 处理sheet为空/只有第一行的情况
        if max_column == 0:
            pass
        else:
            for i in range(1, max_column + 1):
                cellvalue = str(table.cell(1,i).value)
                if cellvalue is None:
                    cellvalue = ""
                colume_info.append(cellvalue)
        file_column_dic[sheet_name] = colume_info
        if max_row <= 1:
            input_file_dic[sheet_name].append(colume_info)
        else:
            for i in range(2, max_row + 1):
                row_info = []
                none_num = 0
                for j in range(1, max_column + 1):
                    cellvalue = str(table.cell(i,j).value)
                    if cellvalue == 'None' or cellvalue.strip(' ') == '':
                        none_num += 1
                        cellvalue = ""
                    row_info.append(cellvalue)
                if none_num == max_column:
                    continue
                input_file_dic[sheet_name].append(row_info)
    return input_file_dic, input_file_sheets, file_column_dic
def get_info_from_excel(input_file_dic, input_file_sheets, file_column_dic, input_file):
    xl = openpyxl.load_workbook(input_file, data_only=True)
    xlsx_sheet_names = xl.sheetnames
    for sheet_name in xlsx_sheet_names:
        #if sheet_name != '总数据表':
            #continue
        table = xl[sheet_name]
        # list [Sheet1, Sheet2]
        input_file_sheets.append(sheet_name)
        # dict {Sheet1: [[1][2][3]], Sheet2: [[1][2][3]]}
        input_file_dic[sheet_name] = []
        # dict {Sheet1: [[0]], Sheet2: [[0]]}
        file_column_dic[sheet_name] = []
        max_row = table.max_row
        max_column = table.max_column
        # 本函数中第一行不为空
        # print(input_file, max_column)
        colume_info = []
        # 处理sheet为空/只有第一行的情况
        if max_column == 0:
            pass
        else:
            for i in range(1, max_column + 1):
                cellvalue = str(table.cell(1,i).value)
                if cellvalue is None:
                    cellvalue = ""
                colume_info.append(cellvalue)
        file_column_dic[sheet_name] = colume_info
        if max_row <= 1:
            input_file_dic[sheet_name].append(colume_info)
        else:
            for i in range(2, max_row + 1):
                row_info = []
                none_num = 0
                for j in range(1, max_column + 1):
                    cellvalue = str(table.cell(i,j).value)
                    if cellvalue == 'None' or cellvalue.strip(' ') == '':
                        none_num += 1
                        cellvalue = ""
                    row_info.append(cellvalue)
                if none_num == max_column:
                    continue
                input_file_dic[sheet_name].append(row_info)
    return input_file_dic, input_file_sheets, file_column_dic
def get_info_from_excel1(input_file_dic, input_file_sheets, file_column_dic, input_file):
    xl = openpyxl.load_workbook(input_file, data_only=True)
    xlsx_sheet_names = xl.sheetnames
    for sheet_name in xlsx_sheet_names:
        table = xl[sheet_name]
        # list [Sheet1, Sheet2]
        input_file_sheets.append(sheet_name)
        # dict {Sheet1: [[1][2][3]], Sheet2: [[1][2][3]]}
        input_file_dic[sheet_name] = []
        # dict {Sheet1: [[0]], Sheet2: [[0]]}
        file_column_dic[sheet_name] = []
        max_row = table.max_row
        max_column = table.max_column
        # 本函数中第一行不为空
        # print(input_file, max_column)
        colume_info = []
        # 处理sheet为空/只有第一行的情况
        if max_column == 0:
            pass
        else:
            for i in range(1, max_column + 1):
                cellvalue = str(table.cell(1,i).value)
                if cellvalue is None:
                    cellvalue = ""
                colume_info.append(cellvalue)
        file_column_dic[sheet_name] = colume_info
        if max_row <= 1:
            input_file_dic[sheet_name].append(colume_info)
        else:
            for i in range(2, max_row + 1):
                row_info = []
                none_num = 0
                for j in range(1, max_column + 1):
                    cellvalue = str(table.cell(i,j).value)
                    if cellvalue == 'None' or cellvalue.strip(' ') == '':
                        none_num += 1
                        cellvalue = ""
                    row_info.append(cellvalue)
                if none_num == max_column:
                    continue
                input_file_dic[sheet_name].append(row_info)
    return input_file_dic, input_file_sheets, file_column_dic

def CenterKPI_to_DB(input_file):
    input_file_dic, input_file_sheets, file_column_dic = {}, [], {}
    input_file_dic, input_file_sheets, file_column_dic = get_info_from_excel2(input_file_dic,
                                                            input_file_sheets, file_column_dic, input_file)
    datas = input_file_dic[input_file_sheets[0]]
    result = {}
    csc_kpi = CSCKPI()
    task = csc_kpi.query.filter_by().all()
    if task:
        for res in task:
            db.session.delete(res)
            db.session.commit()
    center_kpi = CenterKPI()
    task = center_kpi.query.filter_by().all()
    if task:
        for res in task:
            db.session.delete(res)
            db.session.commit()
    index = 0
    input_dic, input_data = {}, []
    for i in range(len(datas)):
        if datas[i][0] == "事故：件":
            valid_data = []
            valid_data.append(['center', '当月', '上海', datas[i][1], datas[i+1][1], datas[i+3][1], datas[i+4][1]])
            valid_data.append(['center', 'YTD', '上海', datas[i][5], datas[i+1][5], datas[i+3][5], datas[i+4][5]])
            valid_data.append(['center', '当月', '武汉', datas[i][2], datas[i+1][2], datas[i+3][2], datas[i+4][2]])
            valid_data.append(['center', 'YTD', '武汉', datas[i][6], datas[i+1][6], datas[i+3][6], datas[i+4][6]])
            valid_data.append(['center', '当月', '成都', datas[i][3], datas[i+1][3], datas[i+3][3], datas[i+4][3]])
            valid_data.append(['center', 'YTD', '成都', datas[i][7], datas[i+1][7], datas[i+3][7], datas[i+4][7]])
            valid_data.append(['center', '当月', '西安', datas[i][4], datas[i+1][4], datas[i+3][4], datas[i+4][4]])
            valid_data.append(['center', 'YTD', '西安', datas[i][8], datas[i+1][8], datas[i+3][8], datas[i+4][8]])
            db.session.execute(csc_kpi.__table__.insert(),
                [{
                    "month": data[1], "city": data[2], "accident": data[3], "complain": data[4],
                    "business_area": data[5], "usable_area": data[6]
                } for data in valid_data]
            )
            db.session.commit()
        if (i <= 9) or ('库存净差异：周' in datas[i]):
            index = i
            continue
        if ('WK' in datas[i][0]) or ('月' in datas[i][0]) or ('YTD' in datas[i][0]):
            if datas[i][0] not in input_dic.keys():
                input_dic[datas[i][0]] = []
                input_dic[datas[i][0]].append(['center', datas[i][0], '上海', datas[i][1], datas[i][5], datas[i][9], datas[i][13], "", "", "", ""])
                input_dic[datas[i][0]].append(['center', datas[i][0], '武汉', datas[i][2], datas[i][6], datas[i][10], datas[i][14], "", "", "", ""])
                input_dic[datas[i][0]].append(['center', datas[i][0], '成都', datas[i][3], datas[i][7], datas[i][11], datas[i][15], "", "", "", ""])
                input_dic[datas[i][0]].append(['center', datas[i][0], '西安', datas[i][4], datas[i][8], datas[i][12], datas[i][16], "", "", "", ""])
    for i in range(index, len(datas)):
        if ('WK' in datas[i][0]) or ('月' in datas[i][0]) or ('YTD' in datas[i][0]):
            if datas[i][0] in input_dic.keys():
                for data in input_dic[datas[i][0]]:
                    if data[2] == '上海':
                        data[7] = datas[i][1]
                        data[8] = datas[i][5]
                        data[9] = datas[i][9]
                        data[10] = datas[i][13]
                    elif data[2] == '武汉':
                        data[7] = datas[i][2]
                        data[8] = datas[i][6]
                        data[9] = datas[i][10]
                        data[10] = datas[i][14]
                    elif data[2] == '成都':
                        data[7] = datas[i][3]
                        data[8] = datas[i][7]
                        data[9] = datas[i][11]
                        data[10] = datas[i][15]
                    elif data[2] == '西安':
                        data[7] = datas[i][4]
                        data[8] = datas[i][8]
                        data[9] = datas[i][12]
                        data[10] = datas[i][16]
    for key in input_dic.keys():
        for data in input_dic[key]:
            input_data.append(data)
    db.session.execute(center_kpi.__table__.insert(),
        [{
            "week": data[1], "city": data[2], "price": data[3], "turnover": data[4],
            "B2C_efficiency": data[5], "B2B_efficiency": data[6], "stock": data[7],
            "performance": data[8], "profit": data[9], "score": data[10]
        } for data in input_data]
    )
    db.session.commit()

def isfloat(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

def kpi_show():
    csc_kpi = CSCKPI()
    center_kpi = CenterKPI()
    [month_mark, week_mark] = get_target_month_week()
    same_task = csc_kpi.query.filter_by(month = "当月").all()
    ytd_task = csc_kpi.query.filter_by(month = "YTD").all()
    result = {}
    if (not same_task) or (not ytd_task):
        return result
    for i in range(4):
        returnDatas = {
            'timeString': '',
            'data': []
        }
        returnData = {
            'noid': '',
            'name': '上海',
            'ytd': 0,
            'num': 0,
            'target': 0
        }
        returnData1 = {
            'noid': '',
            'name': '武汉',
            'ytd': 0,
            'num': 0,
            'target': 0
        }
        returnData2 = {
            'noid': '',
            'name': '成都',
            'ytd': 0,
            'num': 0,
            'target': 0
        }
        returnData3 = {
            'noid': '',
            'name': '西安',
            'ytd': 0,
            'num': 0,
            'target': 0
        }
        if i == 0:
            same_acc, ytd_acc = 0, 0
            for same in same_task:
                if isfloat(same.accident):
                    same_acc = int(float(same.accident))
                if same.city == "上海":
                    returnData['num'] = same_acc
                elif same.city == "武汉":
                    returnData1['num'] = same_acc
                elif same.city == "成都":
                    returnData2['num'] = same_acc
                elif same.city == "西安":
                    returnData3['num'] = same_acc
            for ytd in ytd_task:
                if isfloat(ytd.accident):
                    ytd_acc = int(float(ytd.accident))
                if ytd.city == "上海":
                    returnData['ytd'] = ytd_acc
                elif ytd.city == "武汉":
                    returnData1['ytd'] = ytd_acc
                elif ytd.city == "成都":
                    returnData2['ytd'] = ytd_acc
                elif ytd.city == "西安":
                    returnData3['ytd'] = ytd_acc
            returnDatas['timeString'] = month_mark
            returnDatas['data'].append(returnData)
            returnDatas['data'].append(returnData1)
            returnDatas['data'].append(returnData2)
            returnDatas['data'].append(returnData3)
            result['事故'] = returnDatas
        elif i == 1:
            same_acc, ytd_acc = 0, 0
            for same in same_task:
                if isfloat(same.complain):
                    same_acc = int(float(same.complain))
                if same.city == "上海":
                    returnData['num'] = same_acc
                elif same.city == "武汉":
                    returnData1['num'] = same_acc
                elif same.city == "成都":
                    returnData2['num'] = same_acc
                elif same.city == "西安":
                    returnData3['num'] = same_acc
            for ytd in ytd_task:
                if isfloat(ytd.complain):
                    ytd_acc = int(float(ytd.complain))
                if ytd.city == "上海":
                    returnData['ytd'] = ytd_acc
                elif ytd.city == "武汉":
                    returnData1['ytd'] = ytd_acc
                elif ytd.city == "成都":
                    returnData2['ytd'] = ytd_acc
                elif ytd.city == "西安":
                    returnData3['ytd'] = ytd_acc
            returnDatas['timeString'] = month_mark
            returnDatas['data'].append(returnData)
            returnDatas['data'].append(returnData1)
            returnDatas['data'].append(returnData2)
            returnDatas['data'].append(returnData3)
            result['客户投诉'] = returnDatas
        elif i == 2:
            same_acc, ytd_acc = 0, 0
            for same in same_task:
                if isfloat(same.business_area):
                    same_acc = int(float(same.business_area))
                if same.city == "上海":
                    returnData['num'] = same_acc
                elif same.city == "武汉":
                    returnData1['num'] = same_acc
                elif same.city == "成都":
                    returnData2['num'] = same_acc
                elif same.city == "西安":
                    returnData3['num'] = same_acc
            for ytd in ytd_task:
                if isfloat(ytd.business_area):
                    ytd_acc = int(float(ytd.business_area))
                if ytd.business_area == "/":
                    ytd_acc = "/"
                if ytd.city == "上海":
                    returnData['ytd'] = ytd_acc
                elif ytd.city == "武汉":
                    returnData1['ytd'] = ytd_acc
                elif ytd.city == "成都":
                    returnData2['ytd'] = ytd_acc
                elif ytd.city == "西安":
                    returnData3['ytd'] = ytd_acc
            returnDatas['timeString'] = month_mark
            returnDatas['data'].append(returnData)
            returnDatas['data'].append(returnData1)
            returnDatas['data'].append(returnData2)
            returnDatas['data'].append(returnData3)
            result['可拓展新业务面积'] = returnDatas
        elif i == 3:
            same_acc, ytd_acc = 0, 0
            for same in same_task:
                if isfloat(same.usable_area):
                    same_acc = int(float(same.usable_area))
                if same.city == "上海":
                    returnData['num'] = same_acc
                elif same.city == "武汉":
                    returnData1['num'] = same_acc
                elif same.city == "成都":
                    returnData2['num'] = same_acc
                elif same.city == "西安":
                    returnData3['num'] = same_acc
            for ytd in ytd_task:
                if isfloat(ytd.usable_area):
                    ytd_acc = int(float(ytd.usable_area))
                if ytd.usable_area == "/":
                    ytd_acc = "/"
                if ytd.city == "上海":
                    returnData['ytd'] = ytd_acc
                elif ytd.city == "武汉":
                    returnData1['ytd'] = ytd_acc
                elif ytd.city == "成都":
                    returnData2['ytd'] = ytd_acc
                elif ytd.city == "西安":
                    returnData3['ytd'] = ytd_acc
            returnDatas['timeString'] = month_mark
            returnDatas['data'].append(returnData)
            returnDatas['data'].append(returnData1)
            returnDatas['data'].append(returnData2)
            returnDatas['data'].append(returnData3)
            result['搭平台后可用面积'] = returnDatas
    month_task = center_kpi.query.filter_by(week = month_mark).all()
    week_task = center_kpi.query.filter_by(week = week_mark).all()
    ytd_task = center_kpi.query.filter_by(week = "YTD").all()
    if (not month_task) or (not week_task) or (not ytd_task):
        return result
    for i in range(7):
        returnDatas = {
            'timeString': '',
            'data': []
        }
        returnData = {
            'noid': '',
            'name': '上海',
            'ytd': 0,
            'num': 0,
            'target': 0
        }
        returnData1 = {
            'noid': '',
            'name': '武汉',
            'ytd': 0,
            'num': 0,
            'target': 0
        }
        returnData2 = {
            'noid': '',
            'name': '成都',
            'ytd': 0,
            'num': 0,
            'target': 0
        }
        returnData3 = {
            'noid': '',
            'name': '西安',
            'ytd': 0,
            'num': 0,
            'target': 0
        }
        if i == 0:
            same_acc, ytd_acc = 0, 0
            for same in month_task:
                if isfloat(same.price):
                    same_acc = round(float(same.price), 3)
                if same.city == "上海":
                    returnData['num'] = same_acc
                elif same.city == "武汉":
                    returnData1['num'] = same_acc
                elif same.city == "成都":
                    returnData2['num'] = same_acc
                elif same.city == "西安":
                    returnData3['num'] = same_acc
            for ytd in ytd_task:
                if isfloat(ytd.price):
                    ytd_acc = round(float(ytd.price), 3)
                if ytd.city == "上海":
                    returnData['ytd'] = ytd_acc
                elif ytd.city == "武汉":
                    returnData1['ytd'] = ytd_acc
                elif ytd.city == "成都":
                    returnData2['ytd'] = ytd_acc
                elif ytd.city == "西安":
                    returnData3['ytd'] = ytd_acc
            returnData['target'] = returnData1['target'] = returnData2['target'] = returnData3['target'] = 15
            returnDatas['timeString'] = month_mark
            returnDatas['data'].append(returnData)
            returnDatas['data'].append(returnData1)
            returnDatas['data'].append(returnData2)
            returnDatas['data'].append(returnData3)
            result['单件成本'] = returnDatas
        elif i == 1:
            same_acc, ytd_acc = 0, 0
            for same in month_task:
                if isfloat(same.turnover):
                    same_acc = round(float(same.turnover) * 100, 3)
                if same.city == "上海":
                    returnData['num'] = same_acc
                elif same.city == "武汉":
                    returnData1['num'] = same_acc
                elif same.city == "成都":
                    returnData2['num'] = same_acc
                elif same.city == "西安":
                    returnData3['num'] = same_acc
            for ytd in ytd_task:
                if isfloat(ytd.turnover):
                    ytd_acc = round(float(ytd.turnover) * 100, 3)
                if ytd.city == "上海":
                    returnData['ytd'] = ytd_acc
                elif ytd.city == "武汉":
                    returnData1['ytd'] = ytd_acc
                elif ytd.city == "成都":
                    returnData2['ytd'] = ytd_acc
                elif ytd.city == "西安":
                    returnData3['ytd'] = ytd_acc
            returnData['target'] = returnData1['target'] = returnData2['target'] = returnData3['target'] = 10
            returnDatas['timeString'] = month_mark
            returnDatas['data'].append(returnData)
            returnDatas['data'].append(returnData1)
            returnDatas['data'].append(returnData2)
            returnDatas['data'].append(returnData3)
            result['人员流失率'] = returnDatas
        elif i == 2:
            same_acc, ytd_acc = 0, 0
            for same in week_task:
                if isfloat(same.B2C_efficiency):
                    same_acc = round(float(same.B2C_efficiency), 3)
                if same.city == "上海":
                    returnData['num'] = same_acc
                elif same.city == "武汉":
                    returnData1['num'] = same_acc
                elif same.city == "成都":
                    returnData2['num'] = same_acc
                elif same.city == "西安":
                    returnData3['num'] = same_acc
            for ytd in ytd_task:
                if isfloat(ytd.B2C_efficiency):
                    ytd_acc = round(float(ytd.B2C_efficiency), 3)
                if ytd.city == "上海":
                    returnData['ytd'] = ytd_acc
                elif ytd.city == "武汉":
                    returnData1['ytd'] = ytd_acc
                elif ytd.city == "成都":
                    returnData2['ytd'] = ytd_acc
                elif ytd.city == "西安":
                    returnData3['ytd'] = ytd_acc
            returnData['target'] = returnData1['target'] = returnData2['target'] = returnData3['target'] = 10
            returnDatas['timeString'] = week_mark
            returnDatas['data'].append(returnData)
            returnDatas['data'].append(returnData1)
            returnDatas['data'].append(returnData2)
            returnDatas['data'].append(returnData3)
            result['B2C人均效率'] = returnDatas
        elif i == 3:
            same_acc, ytd_acc = 0, 0
            for same in week_task:
                if isfloat(same.B2B_efficiency):
                    same_acc = round(float(same.B2B_efficiency), 3)
                if same.city == "上海":
                    returnData['num'] = same_acc
                elif same.city == "武汉":
                    returnData1['num'] = same_acc
                elif same.city == "成都":
                    returnData2['num'] = same_acc
                elif same.city == "西安":
                    returnData3['num'] = same_acc
            for ytd in ytd_task:
                if isfloat(ytd.B2B_efficiency):
                    ytd_acc = round(float(ytd.B2B_efficiency), 3)
                if ytd.city == "上海":
                    returnData['ytd'] = ytd_acc
                elif ytd.city == "武汉":
                    returnData1['ytd'] = ytd_acc
                elif ytd.city == "成都":
                    returnData2['ytd'] = ytd_acc
                elif ytd.city == "西安":
                    returnData3['ytd'] = ytd_acc
            returnData['target'] = returnData1['target'] = returnData2['target'] = returnData3['target'] = 60
            returnDatas['timeString'] = week_mark
            returnDatas['data'].append(returnData)
            returnDatas['data'].append(returnData1)
            returnDatas['data'].append(returnData2)
            returnDatas['data'].append(returnData3)
            result['B2B人均效率'] = returnDatas
        elif i == 4:
            same_acc, ytd_acc = 0, 0
            for same in week_task:
                if isfloat(same.stock):
                    same_acc = round(float(same.stock) * 100, 3)
                if same.city == "上海":
                    returnData['num'] = same_acc
                elif same.city == "武汉":
                    returnData1['num'] = same_acc
                elif same.city == "成都":
                    returnData2['num'] = same_acc
                elif same.city == "西安":
                    returnData3['num'] = same_acc
            for ytd in ytd_task:
                if isfloat(ytd.stock):
                    ytd_acc = round(float(ytd.stock) * 100, 3)
                if ytd.city == "上海":
                    returnData['ytd'] = ytd_acc
                elif ytd.city == "武汉":
                    returnData1['ytd'] = ytd_acc
                elif ytd.city == "成都":
                    returnData2['ytd'] = ytd_acc
                elif ytd.city == "西安":
                    returnData3['ytd'] = ytd_acc
            returnDatas['timeString'] = week_mark
            returnData['target'] = returnData1['target'] = returnData2['target'] = returnData3['target'] = 10
            returnDatas['data'].append(returnData)
            returnDatas['data'].append(returnData1)
            returnDatas['data'].append(returnData2)
            returnDatas['data'].append(returnData3)
            result['库存净差异'] = returnDatas
        elif i == 5:
            same_acc, ytd_acc = 0, 0
            for same in month_task:
                if isfloat(same.performance):
                    same_acc = round(float(same.performance) * 100, 3)
                if same.city == "上海":
                    returnData['num'] = same_acc
                elif same.city == "武汉":
                    returnData1['num'] = same_acc
                elif same.city == "成都":
                    returnData2['num'] = same_acc
                elif same.city == "西安":
                    returnData3['num'] = same_acc
            for ytd in ytd_task:
                if isfloat(ytd.performance):
                    ytd_acc = round(float(ytd.performance) * 100, 3)
                if ytd.city == "上海":
                    returnData['ytd'] = ytd_acc
                elif ytd.city == "武汉":
                    returnData1['ytd'] = ytd_acc
                elif ytd.city == "成都":
                    returnData2['ytd'] = ytd_acc
                elif ytd.city == "西安":
                    returnData3['ytd'] = ytd_acc
            returnDatas['timeString'] = month_mark
            returnData['target'] = returnData1['target'] = returnData2['target'] = returnData3['target'] = 50
            returnDatas['data'].append(returnData)
            returnDatas['data'].append(returnData1)
            returnDatas['data'].append(returnData2)
            returnDatas['data'].append(returnData3)
            result['业绩达成率'] = returnDatas
        elif i == 6:
            same_acc, ytd_acc = 0, 0
            for same in month_task:
                if isfloat(same.profit):
                    same_acc = round(float(same.profit) * 100, 3)
                if same.city == "上海":
                    returnData['num'] = same_acc
                elif same.city == "武汉":
                    returnData1['num'] = same_acc
                elif same.city == "成都":
                    returnData2['num'] = same_acc
                elif same.city == "西安":
                    returnData3['num'] = same_acc
            for ytd in ytd_task:
                if isfloat(ytd.profit):
                    ytd_acc = round(float(ytd.profit) * 100, 3)
                if ytd.city == "上海":
                    returnData['ytd'] = ytd_acc
                elif ytd.city == "武汉":
                    returnData1['ytd'] = ytd_acc
                elif ytd.city == "成都":
                    returnData2['ytd'] = ytd_acc
                elif ytd.city == "西安":
                    returnData3['ytd'] = ytd_acc
            returnDatas['timeString'] = month_mark
            returnData['target'] = returnData1['target'] = returnData2['target'] = returnData3['target'] = 30
            returnDatas['data'].append(returnData)
            returnDatas['data'].append(returnData1)
            returnDatas['data'].append(returnData2)
            returnDatas['data'].append(returnData3)
            result['利润率'] = returnDatas
    return result

def kpi_merits(month):
    result = []
    input_file = os.path.join(source_path, '数据.xlsx')
    input_file_dic, input_file_sheets, file_column_dic = {}, [], {}
    input_file_dic, input_file_sheets, file_column_dic = get_info_from_excel1(input_file_dic,
                                                            input_file_sheets, file_column_dic, input_file)
    datas = input_file_dic["工作表" + month]
    data_num = len(datas)
    for i, data in enumerate(datas):
        returnData = {
            'rank': '',
            'name': '',
            'score': '',
            'color': 'red'
        }
        rank = str(data_num - i)
        returnData['rank'] = str(data_num - i)
        returnData['name'] = data[0]
        returnData['score'] = data[1]
        if i < 5:
            returnData['color'] ='green'
        result.append(returnData)
    # print(result)
    return result
def rank_show():
    [month_mark, week_mark] = get_target_month_week()
    center_kpi = CenterKPI()
    tasks = center_kpi.query.filter_by(week=week_mark).all()
    returnDatas = []
    for res in tasks:
        returnData = {
            'city': '',
            'color': '',
            'score': ''
        }
        if res.city == "上海":
            returnData['city'] = "上海"
            returnData['color'] = "red"
            returnData['score'] = res.score
        elif res.city == "武汉":
            returnData['city'] = "武汉"
            returnData['color'] = "orange"
            returnData['score'] = res.score
        elif res.city == "成都":
            returnData['city'] = "成都"
            returnData['color'] = "Cyan"
            returnData['score'] = res.score
        elif res.city == "西安":
            returnData['city'] = "西安"
            returnData['color'] = "blue"
            returnData['score'] = res.score
        returnDatas.append(returnData)
    return [returnDatas]
def TransportKPI_to_DB(input_file):
    print(input_file)
    input_file_dic, input_file_sheets, file_column_dic = {}, [], {}
    input_file_dic, input_file_sheets, file_column_dic = get_info_from_excel(input_file_dic, input_file_sheets, file_column_dic, input_file)
    trans_kpi = TransportKPI()
    task = trans_kpi.query.filter_by().all()
    if task:
        for res in task:
            db.session.delete(res)
            db.session.commit()
    input_data = []
    for sheet in input_file_sheets:
        if (sheet == "总体说明") or sheet == "图表":
            continue
        datas = input_file_dic[sheet]
        temp1,temp2,temp3,temp4,temp5 = [sheet, '一月'],[sheet, '二月'],[sheet, '三月'],[sheet, '四月'],[sheet, '五月']
        temp6,temp7,temp8,temp9,temp10 = [sheet, '六月'],[sheet, '七月'],[sheet, '八月'],[sheet, '九月'],[sheet, '十月']
        temp11,temp12 = [sheet, '十一月'],[sheet, '十二月']
        for i in range(len(datas)):
            if i < 2:
                continue
            temp1.append(datas[i][3])
            temp2.append(datas[i][4])
            temp3.append(datas[i][5])
            temp4.append(datas[i][6])
            temp5.append(datas[i][7])
            temp6.append(datas[i][8])
            temp7.append(datas[i][9])
            temp8.append(datas[i][10])
            temp9.append(datas[i][11])
            temp10.append(datas[i][12])
            temp11.append(datas[i][13])
            temp12.append(datas[i][14])
        input_data += [temp1,temp2,temp3,temp4,temp5,temp6,temp7,temp8,temp9,temp10,temp11,temp12]
    db.session.execute(trans_kpi.__table__.insert(),
        [{
            "project": data[0], "month": data[1], "punctuality": data[2], "availability": data[3],
            "return_rate": data[4], "complaint": data[5], "accident": data[6], "collection_rate": data[7],
            "completion_rate": data[8], "profit_rate": data[9]
        } for data in input_data]
    )
    db.session.commit()
def show_month_transport():
    [month_mark, week_mark] = get_target_month_week()
    trans_kpi = TransportKPI()
    project_names = ['NIKE', 'VF', '阿克苏', '喜利得', '美邦', '京东', '好孩子', '宝胜']
    returnDatas = {
        '交货准时率': {'timeString': month_mark, 'data': []},
        '交货完好率': {'timeString': month_mark, 'data': []},
        '回单返回率': {'timeString': month_mark, 'data': []},
        '客诉次数': {'timeString': month_mark, 'data': []},
        '安全事故次数': {'timeString': month_mark, 'data': []},
        '回款率': {'timeString': month_mark, 'data': []},
        '营业额完成率': {'timeString': month_mark, 'data': []},
        '利润完成率': {'timeString': month_mark, 'data': []},
        '表扬': {'timeString': month_mark, 'data': []},
        '异常分析': month_mark + '异常分析: '
    }
    month = month_mark
    for project in project_names:
        tasks = trans_kpi.query.filter_by(project=project).all()
        cur, ytd, cur1, ytd1, cur2, ytd2, cur3, ytd3 = 0, 0, 0, 0, 0, 0, 0, 0
        cur4, ytd4, cur5, ytd5, cur6, ytd6, cur7, ytd7 = 0, 0, 0, 0, 0, 0, 0, 0
        for task in tasks:
            if task.punctuality:
                if task.month == month:
                    cur = int(task.punctuality)
                ytd += int(task.punctuality)         
            if task.availability:
                if task.month == month:
                    cur1 = int(task.availability)
                ytd1 += int(task.availability)
            if task.return_rate:
                if task.month == month:
                    cur2 = int(task.return_rate)
                ytd2 += int(task.return_rate)
            if task.complaint:
                if task.month == month:
                    cur3 = int(task.complaint)
                ytd3 += int(task.complaint)
            if task.accident:
                if task.month == month:
                    cur4 = int(task.accident)
                ytd4 += int(task.accident)
            if task.collection_rate:
                if task.month == month:
                    cur5 = int(task.collection_rate)
                ytd5 += int(task.collection_rate)
            if task.completion_rate:
                if task.month == month:
                    cur6 = int(task.completion_rate)
                ytd6 += int(task.completion_rate)
            if task.profit_rate:
                if task.month == month:
                    cur7 = int(task.profit_rate)
                ytd7 += int(task.profit_rate)
        returnDatas['交货准时率']['data'].append({'project': project, 'cur': cur, 'ytd': ytd})
        returnDatas['交货完好率']['data'].append({'project': project, 'cur': cur, 'ytd': ytd})
        returnDatas['回单返回率']['data'].append({'project': project, 'cur': cur, 'ytd': ytd})
        returnDatas['客诉次数']['data'].append({'project': project, 'cur': cur, 'ytd': ytd})
        returnDatas['安全事故次数']['data'].append({'project': project, 'cur': cur, 'ytd': ytd})
        returnDatas['回款率']['data'].append({'project': project, 'cur': cur, 'ytd': ytd})
        returnDatas['营业额完成率']['data'].append({'project': project, 'cur': cur, 'ytd': ytd})
        returnDatas['利润完成率']['data'].append({'project': project, 'cur': cur, 'ytd': ytd})
        returnDatas['表扬']['data'].append({'project': project, 'cur': 0, 'ytd': 0})
    return returnDatas
