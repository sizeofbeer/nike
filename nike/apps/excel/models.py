# -*- coding:utf8  -*-
from config import db

''' nike集成功能任务 '''
class NikeTask(db.Model):
    # __tablename__ = "nike_task"
    taskid = db.Column(db.String(50), unique=True, nullable=False, primary_key=True)
    context = db.Column(db.String(50), unique=False, nullable=False)
    service = db.Column(db.String(50), unique=False, nullable=True)
    access = db.Column(db.String(50), unique=False, nullable=False)
    abnormal = db.Column(db.String(50), unique=False, nullable=True)
''' nike个人客户信息 '''
class NikeIndiv(db.Model):
    # __tablename__ = "nike_indiv"
    codetype = db.Column(db.String(50), unique=False, nullable=False)
    soldto = db.Column(db.String(50), unique=False, nullable=False)
    shipto = db.Column(db.String(50), unique=True, nullable=False, primary_key=True)
    billto = db.Column(db.String(50), unique=False, nullable=False)
    name = db.Column(db.String(200), unique=False, nullable=False)
    englishname = db.Column(db.String(200), unique=False, nullable=False)
    address = db.Column(db.String(200), unique=False, nullable=False)
    city = db.Column(db.String(50), unique=False, nullable=False)
    province = db.Column(db.String(50), unique=False, nullable=False)
    region = db.Column(db.String(50), unique=False, nullable=True)
    postalcode = db.Column(db.String(50), unique=False, nullable=True)
    contactor = db.Column(db.String(50), unique=False, nullable=True)
    telephone = db.Column(db.String(50), unique=False, nullable=True)
    opendate = db.Column(db.String(50), unique=False, nullable=True)
    accounttype = db.Column(db.String(50), unique=False, nullable=True)
    storetype = db.Column(db.String(50), unique=False, nullable=True)
    department = db.Column(db.String(50), unique=False, nullable=False)
''' nike进csc门店 '''
class NikeWarehouse(db.Model):
    # __tablename__ = "nike_warehouse"
    storetype = db.Column(db.String(50), unique=False, nullable=False)
    nameabb = db.Column(db.String(50), unique=False, nullable=False)
    shipto = db.Column(db.String(50), unique=True, nullable=False, primary_key=True)
    storename = db.Column(db.String(50), unique=False, nullable=False)
    dohwindow = db.Column(db.String(50), unique=False, nullable=True)
    dohtime = db.Column(db.String(50), unique=False, nullable=True)
    cscname = db.Column(db.String(50), unique=False, nullable=True)
''' nike ob 太仓报价 '''
class NikeRoad(db.Model):
    # __tablename__ = "nike_road"
    city = db.Column(db.String(50), unique=True, nullable=False, primary_key=True)
    province = db.Column(db.String(50), unique=False, nullable=False)
    citytier = db.Column(db.String(50), unique=False, nullable=True)
    std1 = db.Column(db.String(50), unique=False, nullable=False)
    std2 = db.Column(db.String(50), unique=False, nullable=False)
    std3 = db.Column(db.String(50), unique=False, nullable=False)
    std4 = db.Column(db.String(50), unique=False, nullable=False)
    std5 = db.Column(db.String(50), unique=False, nullable=False)
    leadtime = db.Column(db.String(50), unique=False, nullable=True)
''' nike ob 太仓dtc报价 '''
class NikeDtc(db.Model):
    # __tablename__ = "nike_dtc"
    city = db.Column(db.String(50), unique=True, nullable=False, primary_key=True)
    province = db.Column(db.String(50), unique=False, nullable=False)
    citytier = db.Column(db.String(50), unique=False, nullable=True)
    std1 = db.Column(db.String(50), unique=False, nullable=False)
    std2 = db.Column(db.String(50), unique=False, nullable=False)
    std3 = db.Column(db.String(50), unique=False, nullable=False)
    std4 = db.Column(db.String(50), unique=False, nullable=False)
    std5 = db.Column(db.String(50), unique=False, nullable=False)
    leadtime = db.Column(db.String(50), unique=False, nullable=True)
''' nike ob bzbj报价 '''
class NikeBzbj(db.Model):
    # __tablename__ = "nike_bzbj"
    city = db.Column(db.String(50), unique=True, nullable=False, primary_key=True)
    province = db.Column(db.String(50), unique=False, nullable=False)
    citytier = db.Column(db.String(50), unique=False, nullable=True)
    std1 = db.Column(db.String(50), unique=False, nullable=False)
    std2 = db.Column(db.String(50), unique=False, nullable=False)
    std3 = db.Column(db.String(50), unique=False, nullable=False)
    std4 = db.Column(db.String(50), unique=False, nullable=False)
    std5 = db.Column(db.String(50), unique=False, nullable=False)
    leadtime = db.Column(db.String(50), unique=False, nullable=True)
    returntime = db.Column(db.String(50), unique=False, nullable=True)
    epodtime = db.Column(db.String(50), unique=False, nullable=True)
''' nike ob bzbj-dtc报价 '''
class NikeBzbjDtc(db.Model):
    # __tablename__ = "nike_bzbj_dtc"
    city = db.Column(db.String(50), unique=True, nullable=False, primary_key=True)
    province = db.Column(db.String(50), unique=False, nullable=False)
    citytier = db.Column(db.String(50), unique=False, nullable=True)
    std1 = db.Column(db.String(50), unique=False, nullable=False)
    std2 = db.Column(db.String(50), unique=False, nullable=False)
    std3 = db.Column(db.String(50), unique=False, nullable=False)
    std4 = db.Column(db.String(50), unique=False, nullable=False)
    std5 = db.Column(db.String(50), unique=False, nullable=False)
    leadtime = db.Column(db.String(50), unique=False, nullable=True)
    returntime = db.Column(db.String(50), unique=False, nullable=True)
    epodtime = db.Column(db.String(50), unique=False, nullable=True)
''' nike ob 空运报价 '''
class NikeAir(db.Model):
    # __tablename__ = "nike_air"
    city = db.Column(db.String(50), unique=True, nullable=False, primary_key=True)
    province = db.Column(db.String(50), unique=False, nullable=False)
    citytier = db.Column(db.String(50), unique=False, nullable=True)
    std1 = db.Column(db.String(50), unique=False, nullable=False)
    std2 = db.Column(db.String(50), unique=False, nullable=False)
    std3 = db.Column(db.String(50), unique=False, nullable=False)
    leadtime = db.Column(db.String(50), unique=False, nullable=True)
''' nike 仓库地址 '''
class NikeDc(db.Model):
    # __tablename__ = "nike_dc"
    name = db.Column(db.String(50), unique=True, nullable=False, primary_key=True)
    address = db.Column(db.String(50), unique=False, nullable=False)
''' nike 门店doh时间 '''
class NikeDtcTime(db.Model):
    # __tablename__ = "nike_dtc_time"
    consignee = db.Column(db.String(50), unique=False, nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False, primary_key=True)
    storetype = db.Column(db.String(50), unique=False, nullable=False)
    iscsc = db.Column(db.String(50), unique=False, nullable=True)
    address = db.Column(db.String(200), unique=False, nullable=False)
    requestdoh = db.Column(db.String(50), unique=False, nullable=True)
    actualltime = db.Column(db.String(50), unique=False, nullable=True)
''' nike 责任原因 '''
class NikeReason(db.Model):
    # __tablename__ = "nike_reason"
    reasoncode = db.Column(db.String(50), unique=True, nullable=False, primary_key=True)
    belong = db.Column(db.String(50), unique=False, nullable=False)
    describe = db.Column(db.String(50), unique=False, nullable=False)

# 创建数据库表
db.create_all()