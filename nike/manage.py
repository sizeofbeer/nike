from flask_restful import Api
from apps.user import regist_user
from apps.ocr import regist_ocr
from apps.excel import regist_excel
from apps.email import regist_email
from apps.kpi import regist_kpi
from config import app
from flask_script import Manager

api = Api(app)
regist = [rg(api) for rg in [regist_user, regist_ocr, regist_excel, regist_email, regist_kpi]]
manager = Manager(app)

if __name__ == '__main__':
    # app.run(host="192.168.15.57", port= "1887")
    manager.run()
    # gunicorn -c gun.py manage:app
