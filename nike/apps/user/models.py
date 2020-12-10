# -*- coding:utf8  -*-
from config import db, app
import jwt, time
''' nike系统用户登录 '''
class NikeLoginconf(db.Model):     # 基础配置表
    # __tablename__ = "nike_loginconf"
    username = db.Column(db.String(50), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(50), unique=False, nullable=False)
    authority = db.Column(db.String(50), unique=False, nullable=False)
    def generate_auth_token(self, expires_in=600):
        return jwt.encode(
            {'name': self.username, 'exp': time.time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'],
                              algorithms=['HS256'])
        except:
            return None
        return NikeLoginconf.query.get(data['name'])

# 创建数据库表
db.create_all()
