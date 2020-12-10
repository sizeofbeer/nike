# -*- coding:utf8  -*-
from config import db

''' nike 绩效排名 '''
class CSCKPI(db.Model):
    # __tablename__ = "csc_kpi"
    noid = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    month = db.Column(db.String(50), unique=False, nullable=False)
    city = db.Column(db.String(50), unique=False, nullable=False)
    accident = db.Column(db.String(50), unique=False, nullable=False)
    complain = db.Column(db.String(50), unique=False, nullable=False)
    business_area = db.Column(db.String(50), unique=False, nullable=False)
    usable_area = db.Column(db.String(50), unique=False, nullable=False)
''' 中台表格展示 '''
class CenterKPI(db.Model):
    # __tablename__ = "center_kpi"
    noid = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    week = db.Column(db.String(50), unique=False, nullable=False)
    city = db.Column(db.String(50), unique=False, nullable=False)
    price = db.Column(db.String(50), unique=False, nullable=False)
    turnover = db.Column(db.String(50), unique=False, nullable=False)
    B2C_efficiency = db.Column(db.String(50), unique=False, nullable=False)
    B2B_efficiency = db.Column(db.String(50), unique=False, nullable=False)
    stock = db.Column(db.String(50), unique=False, nullable=False)
    performance = db.Column(db.String(50), unique=False, nullable=False)
    profit = db.Column(db.String(50), unique=False, nullable=False)
    score = db.Column(db.String(50), unique=False, nullable=False)
class TransportKPI(db.Model):
    # __tablename__ = "center_kpi"
    noid = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    project = db.Column(db.String(50), unique=False, nullable=False)
    month = db.Column(db.String(50), unique=False, nullable=False)
    punctuality = db.Column(db.String(50), unique=False, nullable=False)
    availability = db.Column(db.String(50), unique=False, nullable=False)
    return_rate = db.Column(db.String(50), unique=False, nullable=False)
    complaint = db.Column(db.String(50), unique=False, nullable=False)
    accident = db.Column(db.String(50), unique=False, nullable=False)
    collection_rate = db.Column(db.String(50), unique=False, nullable=False)
    completion_rate = db.Column(db.String(50), unique=False, nullable=False)
    profit_rate = db.Column(db.String(50), unique=False, nullable=False)

# 创建数据库表
db.create_all()
