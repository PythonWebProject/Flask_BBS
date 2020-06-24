from wtforms import Form, StringField
from wtforms.validators import InputRequired, regexp
import hashlib

class SMSCaptchaForm(Form):
    telephone = StringField(validators=[regexp(r'1[3-9]\d{9}')])
    timestamp = StringField(validators=[regexp(r'\d{13}')])
    sign = StringField(validators=[InputRequired()])

    def validate_sign(self, field):
        '''验证前端发送过来的sign与后端用同样的加密方式生成的sign是否一致'''
        telephone = self.telephone.data
        timestamp = self.timestamp.data
        # 前端传来的sign
        sign = self.sign.data
        # 后端生成的sign
        sign2 = hashlib.md5((timestamp + telephone + "q3423805gdflvbdfvhsdoa`#$%").encode('utf-8')).hexdigest()
        print('Client Sign:', sign)
        print('Server Sign:', sign2)

        if sign == sign2:
            return True
        else:
            return False