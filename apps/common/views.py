from flask import Blueprint, request
from utils import send_msg, restful
from utils.captcha import Captcha
from .forms import SMSCaptchaForm
from utils import clcache

common_bp = Blueprint('common', __name__, url_prefix='/c')


@common_bp.route('/sms_captcha/', methods=['POST'])
def sms_captcha():
    form = SMSCaptchaForm(request.form)

    if form.validate():
        telephone = form.telephone.data
        captcha = Captcha.gene_text(4)
        print('发送的短信验证码：{}'.format(captcha))
        if send_msg.send_mobile_msg(telephone, captcha) == 0:
            clcache.save_captcha(telephone, captcha)
            return restful.success()
        else:
            return restful.params_error(message='发送失败')
    else:
        return restful.params_error(message='参数错误')