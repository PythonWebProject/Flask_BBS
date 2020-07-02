from flask import Blueprint, request, jsonify
from qiniu import Auth
from datetime import datetime
import os

from utils import send_msg, restful
from utils.captcha import Captcha
from .forms import SMSCaptchaForm
from utils import clcache
from utils.random_captcha import get_random_captcha
from exts import qiniu_store, csrf
from config import QINIU_ACCESS_KEY, QINIU_SECRET_KEY

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
    q = Auth(QINIU_ACCESS_KEY, QINIU_SECRET_KEY)
    # 要上传的空间
    bucket_name = 'bbs-images'
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name)

    return jsonify({'uptoken':token})


@common_bp.route('/edittoken/', methods=['POST'])
@csrf.exempt
def edittoken():
    data = request.files['editormd-image-file']
    if not data:
        res = {
            'success': 0,
            'message': 'upload failed'
        }
    else:
        ex = os.path.splitext(data.filename)[1]
        filename = datetime.now().strftime('%Y%m%d%H%M%S') + '-' + get_random_captcha(4) + ex
        file = data.stream.read()
        qiniu_store.save(file, filename)
        print(qiniu_store._base_url)
        print(filename)
        print(qiniu_store.url(filename))
        res = {
            'success': 1,
            'message': 'upload success',
            'url': qiniu_store.url(filename)
        }

    return jsonify(res)