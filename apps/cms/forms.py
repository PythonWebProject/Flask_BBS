from wtforms import Form, StringField, IntegerField, ValidationError
from wtforms.validators import Email, InputRequired, Length, EqualTo, URL
from utils import clcache


class BaseForm(Form):
    def get_error(self):
        message = self.errors.popitem()[1][0]
        return message


class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确的邮箱地址'), InputRequired(message='请输入邮箱')])
    password = StringField(validators=[Length(6, 20, message='密码长度应介于6-20')])
    remember = IntegerField()


class ResetPwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6, 20, message='密码长度应介于6-20')])
    newpwd = StringField(validators=[Length(6, 20, message='密码长度应介于6-20')])
    newpwd2 = StringField(validators=[EqualTo("newpwd", message='两次输入密码不一致')])


class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email(message='您的邮箱格式有误，请重新输入')])
    captcha = StringField(validators=[Length(4, 4, message='请输入4位验证码')])

    def validate_captcha(self, form):
        captcha = self.captcha.data
        email = self.email.data
        redis_captcha = clcache.get_captcha(email)
        if not redis_captcha or captcha.lower() != redis_captcha.lower():
            raise ValidationError('邮箱验证码错误')


class AddBannerForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入轮播图名称')])
    image_url = StringField(validators=[InputRequired(message='请输入图片链接'), URL(message='请注意图片链接格式')])
    link_url = StringField(validators=[InputRequired(message='请输入跳转链接'), URL(message='请注意跳转链接格式')])
    priority = IntegerField(validators=[InputRequired(message='请输入轮播图优先级')])


class UpdateBannerForm(AddBannerForm):
    banner_id = IntegerField(validators=[InputRequired(message='轮播图不存在')])