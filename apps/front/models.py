import shortuuid
import enum
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from exts import db


class GenderEnum(enum.Enum):
    MALE = 1
    FAMALE = 2
    SECRET = 3
    UNKNOWN = 4


class FrontUser(db.Model):
    __tablename__ = 'front_user'
    id = db.Column(db.String(40), primary_key=True, default=shortuuid.uuid)
    telephone = db.Column(db.String(11), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=False)
    realname = db.Column(db.String(30))
    avatar = db.Column(db.String(80))
    signature = db.Column(db.String(200))
    gender = db.Column(db.Enum(GenderEnum), default=GenderEnum.UNKNOWN)

    join_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, *args, **kwargs):
        if 'password' in kwargs:
            self.password = kwargs.get('password')
            kwargs.pop('password')

        super().__init__(*args, **kwargs)

    @property
    def password(self):
        '''获取密码'''
        return self._password

    @password.setter
    def password(self, raw_password):
        '''设置密码'''
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        '''验证密码是否正确'''
        result = check_password_hash(self.password, raw_password)
        return result
