from flask import Flask
from flask_cors import CORS
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

cors = CORS(app)
app.config['WEB_URL'] = 'http://xiaolin.vaiwan.com'
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@192.168.15.77:3306/nike?charset=utf8'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_POOL_SIZE'] = 10
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 5

db = SQLAlchemy(app)
