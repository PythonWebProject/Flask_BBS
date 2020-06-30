from flask import Blueprint, request, jsonify
from qiniu import Auth, put_file, etag

from utils import send_msg, restful
from utils.captcha import Captcha
from .forms import SMSCaptchaForm
from utils import clcache
from config import QN_AK, QN_SK

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


@common_bp.route('/uptoken/')
def uptoken():
    # 构建鉴权对象
    q = Auth(QN_AK, QN_SK)
    # 要上传的空间
    bucket_name = 'corley-images'
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name)

    return jsonify({'uptoken':token})