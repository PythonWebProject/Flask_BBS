from flask import Blueprint, views, render_template, make_response, request, session
from io import BytesIO

from utils.captcha import Captcha
from utils import clcache, restful, safe_url
from .forms import SignupForm, SigninForm
from .models import FrontUser
from apps.cms.models import BannerModel
from exts import db

front_bp = Blueprint('front', __name__)


@front_bp.route('/')
def index():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(4)
    return render_template('front/front_index.html', banners=banners)


@front_bp.route('/captcha/')
def graph_captcha():
    try:
        text, image = Captcha.gene_graph_captcha()
        print('发送的图形验证码：{}'.format(text))
        clcache.save_captcha(text.lower(), text)
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


@front_bp.route('/referer_test/')
def referer_test():
    return render_template('front/referer_test.html')


class SignupView(views.MethodView):
    def get(self):
        # referrer表示页面的跳转，即从哪个页面跳转到当前页面
        print('Referer:', request.referrer)
        return_to = request.referrer
        # is_safe_url()判断请求是否来自站内
        if return_to and return_to != request.url and safe_url.is_safe_url(return_to):
            return render_template('front/front_signup.html',return_to=return_to)
        else:
            return render_template('front/front_signup.html')

    def post(self):
        form = SignupForm(request.form)
        if form.validate():
            # 验证成功则保存数据
            telephone = form.telephone.data
            username = form.username.data
            password = form.password1.data

            user = FrontUser(telephone=telephone, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return restful.success(message='注册成功，欢迎您进入熊熊论坛')
        else:
            return restful.params_error(message=form.get_error())


class SigninView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and safe_url.is_safe_url(return_to):
            return render_template('front/front_signin.html', return_to=return_to)
        else:
            return render_template('front/front_signin.html')

    def post(self):
        form = SigninForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remember.data
            user = FrontUser.query.filter_by(telephone=telephone).first()
            if user and user.check_password(password):
                session['user_id'] = user.id
                if remember:
                    session.permanent = True
                return restful.success(message='登录成功')
            else:
                return restful.params_error(message='手机号或密码有误')
        else:
            return restful.params_error(message=form.get_error())


front_bp.add_url_rule('/signup/', view_func=SignupView.as_view('signup'))
front_bp.add_url_rule('/signin/', view_func=SigninView.as_view('signin'))
