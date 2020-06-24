from flask import Blueprint, request
from utils import send_msg, restful
from utils.captcha import Captcha
from .forms import SMSCaptchaForm

common_bp = Blueprint('common', __name__, url_prefix='/c')


@common_bp.route('/sms_captcha/', methods=['POST'])
def sms_captcha():
    form = SMSCaptchaForm(request.form)
    
    if form.validate():
        return restful.success()
    else:
        return restful.params_error(message='参数错误')
    
    '''
    telephone = request.form.get('telephone')
    if not telephone:
        return restful.params_error(message='请填写手机号码')

    captcha = Captcha.gene_text(4)
    if send_msg.send_mobile_msg(telephone, captcha) == 0:
        return restful.success()
    else:
        return restful.params_error(message='发送失败')
    '''