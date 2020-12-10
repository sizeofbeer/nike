# -*- coding:utf8  -*-
from config import db

''' 喜利得表单OCR '''
class Ocr_Hilti(db.Model):     # 货单验收定位表
    # __tablename__ = "ocr_hilti"
    ocrresult = db.Column(db.String(50), unique=True, nullable=False, primary_key=True)
    ocrcount = db.Column(db.String(50), unique=False, nullable=False)

# 创建数据库表
db.create_all()
