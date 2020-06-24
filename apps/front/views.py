from flask import Blueprint, views, render_template, make_response
from io import BytesIO

from utils.captcha import Captcha

front_bp = Blueprint('front', __name__)


@front_bp.route('/')
def index():
    return '前台首页'


@front_bp.route('/captcha/')
def graph_captcha():
    try:
        text, image = Captcha.gene_graph_captcha()
        # 处理图片二进制流的传输
        out = BytesIO()
        # 把图片保存到字节流中，并指定格式为png
        image.save(out, 'png')
        # 指定文件流指针,从文件最开始开始读
        out.seek(0)
        # 将字节流包装到Response对象中,返回前端
        resp = make_response(out.read())
        resp.content_type = 'image/png'
    except:
        return graph_captcha()

    return resp


class SignupView(views.MethodView):
    def get(self):
        return render_template('front/front_signup.html')


front_bp.add_url_rule('/signup/', view_func=SignupView.as_view('signup'))
