# -*- coding:utf8  -*-
from flask_restful import Resource
from flask import request
from apps.user.models import *

''' 用户登录/管理 '''
class NikeLogin(Resource):
    def post(self):
        returnData = {
            'status': 0,
            'msg': '',
            'token': ''
        }
        try:
            key_dict = request.json
            name = key_dict['user']
            psd = key_dict['password']
            print(key_dict)
            User = NikeLoginconf()
            user = User.query.filter_by(username=name).first()
            if not user:
                returnData['msg'] = '用户未注册'
                return returnData
            if user.password == psd:
                token = user.generate_auth_token(7200)
                token = str(token, encoding="utf8")
                # print(token)
                returnData['msg'] = '用户登录成功'
                returnData['token'] = token
                returnData['status'] = 1
            else:
                returnData['msg'] = '用户密码错误'
            return returnData
        except Exception as error:
            returnData['msg'] = str(error)
            return returnData
class CheckLogin(Resource):
    def post(self):
        returnData = {
            'status': 0,
            'msg': ''
        }
        try:         
            token = request.headers.get('token')
            print(token)
            User = NikeLoginconf()
            user = User.verify_auth_token(token)
            print(user)
            if not user:
                returnData['msg'] = "token验证错误"
                return returnData
            returnData['status'] = 1
            returnData['msg'] = "token验证成功"
            return returnData
        except Exception as error:
            returnData['msg'] = str(error)
            return returnData
class Insert_User(Resource):
    def post(self):
        returnData = {
            "msg": "",
            "status": 0
        }
        valid_data = []
        key_dict = request.json
        token = request.headers.get('token')
        user_data = key_dict['res']
        # print(key_dict)
        valid_data.append([user_data['username'], user_data['password'], user_data['authority']])
        # print(valid_data)
        # print(token)
        User = NikeLoginconf()
        user = User.verify_auth_token(token)
        try:
            if not user:
                returnData['msg'] = 'token异常'
                return returnData
            if user.authority == "管理员":
                task = User.query.filter_by(username = valid_data[0][0]).first()
                # print(task.username)
                if not task:
                    db.session.execute(User.__table__.insert(),
                        [{
                            "username": data[0], "password": data[1], "authority": data[2]
                        } for data in valid_data]
                    )
                    db.session.commit()
                    returnData['msg'] = '添加用户成功'
                    returnData["status"] = 1
                else:
                    returnData['msg'] = '用户已存在, 请进行更新操作'
            else:
                returnData['msg'] = '无权限添加用户'
            return returnData
        except Exception as error:
            returnData['msg'] = str(error)
            return returnData
class Search_User(Resource):
    def get(self):
        returnData = {
            'oneself': [],
            'others': [],
            'author': "",
            "msg": "",
            "status": 0
        }
        token = request.headers.get('token')
        # print(token)
        User = NikeLoginconf()
        user = User.verify_auth_token(token)
        try:
            if not user:
                returnData['msg'] = 'token异常'
                return returnData
            if user.authority == "管理员":
                filters = {}
                task = User.query.filter_by(**filters).all()
                for ele in task:
                    if ele.username == user.username:
                        returnData['oneself'].append({
                            "username": ele.username, "password": "", "authority": ele.authority
                        })
                    else:
                        returnData['others'].append({
                            "username": ele.username, "password": ele.password, "authority": ele.authority
                        })
            else:
                returnData['oneself'].append({
                    "username": user.username, "password": "", "authority": user.authority
                })
            returnData['author'] = user.authority
            returnData['msg'] = '查询用户成功'
            returnData['status'] = 1
            # print(returnData)
            return returnData
        except Exception as error:
            returnData['msg'] = str(error)
            return returnData
class Delete_User(Resource):
    def post(self):
        returnData = {
            "msg": "",
            "status": 0
        }
        key_dict = request.json
        valid_data = []
        # print(key_dict)
        token = request.headers.get('token')
        resdata = key_dict['others']
        for res in resdata:
            valid_data.append([res["username"], res["password"], res["authority"]])
        # print(token)
        User = NikeLoginconf()
        user = User.verify_auth_token(token)
        try:
            if not user:
                returnData['msg'] = 'token异常'
                return returnData
            if user.authority == "管理员":
                for ele in valid_data:
                    if ele[2] != "管理员":
                        task = User.query.filter_by(username = ele[0]).first()
                        db.session.delete(task)
                        db.session.commit()
                returnData['msg'] = '删除用户成功'
                returnData['status'] = 1
            else:
                returnData['msg'] = '无权限删除用户'
            return returnData
        except Exception as error:
            returnData['msg'] = str(error)
            return returnData
class Update_User(Resource):
    def post(self):
        returnData = {
            "msg": "",
            "status": 0
        }
        key_dict = request.json
        token = request.headers.get('token')
        user_data = key_dict['res']
        valid_data = []
        old_psd = user_data['oldpassword']
        # print(user_data)
        # print(old_psd)
        User = NikeLoginconf()
        user = User.verify_auth_token(token)
        if user.username == user_data["username"]:
            valid_data.append([user_data["username"], user_data["password"]])
        else:
            valid_data.append([user_data["username"], user_data["password"], user_data["authority"]])
        try:
            if not user:
                returnData['msg'] = 'token异常'
                return returnData
            if valid_data:
                if user.password != old_psd:
                    returnData['msg'] = '旧密码错误, 请重新尝试'
                    return returnData
                keys = ["username", "password", "authority"]
                keys1 = ["username", "password"]
                for ele in valid_data:
                    if user.username == ele[0]:
                        filters = {}
                        for i in range(len(keys1)):
                            filters[keys1[i]] = ele[i]
                        res = User.query.filter_by(username = ele[0]).update(filters)
                        db.session.commit()
                    else:
                        filters = {}
                        for i in range(len(keys)):
                            filters[keys[i]] = ele[i]
                        res = User.query.filter_by(username = ele[0]).update(filters)
                        db.session.commit()
            returnData['msg'] = '更新用户成功'
            returnData['status'] = 1
            return returnData
        except Exception as error:
            returnData['msg'] = str(error)
            return returnData