from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from exts import db


class CMSUser(db.Model):
    '''后台管理员用户类'''
    __tablename__ = 'cms_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

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


class CMSPermission(object):
    # 255二进制表示所有权限
    ALL_PERMISSION = 0b11111111

    # 访问权限
    VISITOR = 0b00000001

    # 管理帖子权限
    POSTER = 0b00000010

    # 管理评论权限
    COMMENTER = 0b00000100

    # 管理板块
    BOARDER = 0b00001000

    # 管理前台用户
    FRONTUSER = 0b00010000

    # 管理前台用户
    CMSUSER = 0b00100000

    # 管理前台用户
    ADMINER = 0b01000000


cms_role_user = db.Table(
    'cms_role_user',
    db.Column('cms_role_id', db.Integer, db.ForeignKey('cms_role.id'), primary_key=True),
    db.Column('cms_user_id', db.Integer, db.ForeignKey('cms_user.id'), primary_key=True)
)


class CMSRole(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now())
    permissions = db.Column(db.Integer, default=CMSPermission.VISITOR)

    users = db.relationship('CMSUser', secondary=cms_role_user, backref='roles')