from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_qiniustorage import Qiniu
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()

mail = Mail()

qiniu_store = Qiniu()

csrf = CSRFProtect()