import shortuuid
import enum
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from markdown import markdown
import bleach

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


class PostModel(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    content_html = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now)

    board_id = db.Column(db.Integer, db.ForeignKey("cms_board.id"))
    author_id = db.Column(db.String(40), db.ForeignKey("front_user.id"))
    # 1表示被删除，0表示未删除，默认为0
    is_delete = db.Column(db.Integer, default=0)

    board = db.relationship("BoardModel", backref='posts')
    author = db.relationship("FrontUser", backref='posts')

    def on_changed_content(target, value, oldvalue, initiator):
        '''实现markdown转HTML并进行安全验证'''
        # 允许上传的标签
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'img', 'video', 'div', 'iframe', 'p', 'br', 'span', 'hr', 'src', 'class']

        # 允许上传的属性
        allowed_attrs = {'*': ['class'],
                         'a': ['href', 'rel'],
                         'img': ['src', 'alt']}

        # 目标设置
        target.content_html = bleach.linkify(
            bleach.clean(markdown(value, output_format='html'), tags=allowed_tags, strip=True,
                         attributes=allowed_attrs))


# 数据库事件监听
db.event.listen(PostModel.content, 'set', PostModel.on_changed_content)


class CommentModel(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    
    commenter_id = db.Column(db.String(40), db.ForeignKey('front_user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    # 1表示被删除，0表示未删除，默认为0
    is_delete = db.Column(db.Integer, default=0)

    post = db.relationship('PostModel', backref='comments')
    commenter = db.relationship('FrontUser', backref='comments')