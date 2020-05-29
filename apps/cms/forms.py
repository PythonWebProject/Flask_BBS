from wtforms import Form, StringField, IntegerField
from wtforms.validators import Email, InputRequired, Length, EqualTo


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