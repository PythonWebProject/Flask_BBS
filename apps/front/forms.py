from wtforms import Form, StringField, ValidationError
from wtforms.validators import Length, EqualTo, Regexp, InputRequired
from utils import clcache


class BaseForm(Form):
    def get_error(self):
        message = self.errors.popitem()[1][0]
        return message


class SignupForm(BaseForm):
    telephone = StringField(validators=[Regexp(r'1[3-9]\d{9}', message='请输入正确的手机号')])
    sms_captcha = StringField(validators=[Regexp(r'\w{4}', message='请输入4位短信验证码')])
    username = StringField(validators=[Length(min=2, max=20, message='用户名应介于2-20个字符，请重新输入')])
    password1 = StringField(validators=[Regexp(r'[0-9a-zA-Z_\.]{6,20}', message='密码应介于6-20位，并且由数字、英文字母或下划线、英文句号或短横线组成')])
    password2 = StringField(validators=[EqualTo('password1', message='两次输入密码不一致')])
    graph_captcha = StringField(validators=[Regexp(r'\w{4}', message='请输入4位图形验证码')])

    def validate_sms_captcha(self, field):
        telephone = self.telephone.data
        sms_captcha = self.sms_captcha.data

        # 从Redis中取验证码
        sms_captcha_redis = clcache.get_captcha(telephone)
        if not sms_captcha_redis or sms_captcha_redis.lower() != sms_captcha.lower():
            raise ValidationError(message='短信验证码过期或有误')

    def validate_graph_captcha(self, field):
        graph_captcha = self.graph_captcha.data
        
        # 从Redis中取图形验证码
        graph_captcha_redis = clcache.get_captcha(graph_captcha.lower())
        if not graph_captcha_redis or graph_captcha_redis.lower() != graph_captcha.lower():
            raise ValidationError(message='图形验证码过期或有误')


class SigninForm(BaseForm):
    telephone = StringField(validators=[Regexp(r'1[3-9]\d{9}', message='请输入正确的手机号')])
    password = StringField(validators=[Regexp(r'[0-9a-zA-Z_\.]{6,20}', message='您输入的密码有误，请重新输入')])
    remember = StringField(InputRequired())