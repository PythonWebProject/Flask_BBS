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

    @property
    def permissions(self):
        '''判断用户权限'''
        if not self.roles:
            return 0

        all_permissions = 0
        for role in self.roles:
            permissions = role.permissions
            all_permissions |= permissions
        return all_permissions

    def has_permission(self, permission):
        '''判断当前用户是否有某个权限'''
        all_permissions = self.permissions
        result = all_permissions & permission == permission  # 如果当前用户有某个权限，则他的全部权限与该权限按位与的结果等于该权限本身
        return result

    @property
    def is_developer(self):
        '''判断当前用户是否是开发人员'''
        return self.has_permission(CMSPermission.ALL_PERMISSION)


class CMSPermission(object):
    # 255二进制表示所有权限
    ALL_PERMISSION = 0b11111111

    # 访问权限
    VISITOR = 0b00000001

    # 管理帖子权限
    POSTER = 0b00000010

    # 管理轮播图
    BANNER = 0b00000100

    # 管理评论权限
    COMMENTER = 0b00001000

    # 管理板块
    BOARDER = 0b00010000

    # 管理前台用户
    FRONTUSER = 0b00100000

    # 管理前台用户
    CMSUSER = 0b01000000

    # 管理前台用户
    ADMINER = 0b10000000


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


class BannerModel(db.Model):
    __tablename__ = 'banner'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    # 图片链接
    image_url = db.Column(db.String(255), nullable=False)
    # 跳转链接
    link_url = db.Column(db.String(255), nullable=False)
    # 优先级
    priority = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)
    # 1表示被删除，0表示未删除，默认为0
    is_delete = db.Column(db.Integer, default=0)


class BoardModel(db.Model):
    __tablename__ = 'cms_board'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    # 1表示被删除，0表示未删除，默认为0
    is_delete = db.Column(db.Integer, default=0)


class HighlightPostModel(db.Model):
    __tablename__ = 'highlight_post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    create_time = db.Column(db.DateTime, default=datetime.now)

    post = db.relationship('PostModel', backref='highlight')