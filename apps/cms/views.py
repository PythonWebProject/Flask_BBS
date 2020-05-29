from flask import Blueprint, render_template, views, request, redirect, url_for, session, g
from apps.cms.forms import LoginForm, ResetPwdForm
from apps.cms.models import CMSUser
from exts import db
from utils import restful

# from .decorators import login_required  # .代表当前路径

cms_bp = Blueprint('cms', __name__, url_prefix='/cms')

from .hooks import before_request


@cms_bp.route('/')
# @login_required
def index():
    return render_template('cms/cms_index.html')


@cms_bp.route('/logout/')
def logout():
    # 清空session
    del session['user_id']
    # 重定向到登录页面
    return redirect(url_for('cms.login'))


@cms_bp.route("/profile/")
def profile():
    return render_template("cms/cms_profile.html")


class LoginView(views.MethodView):
    def get(self, message=None):
        return render_template('cms/cms_login.html', message=message)

    def post(self):
        login_form = LoginForm(request.form)
        # 判断表单是否验证
        if login_form.validate():
            # 获取数据
            email = login_form.email.data
            password = login_form.password.data
            remember = login_form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            # 根据用户验证密码是否正确
            if user and user.check_password(password):
                # 将用户id记录入session
                session['user_id'] = user.id
                # 如果记住密码，需要持久化
                if remember:
                    session.permanent = True
                # 登录成功，则跳转到后台首页
                return redirect(url_for('cms.index'))
            else:
                return self.get(message='邮箱或密码有误')
        else:
            print(login_form.errors)
            return self.get(message=login_form.get_error())


class ResetPwdView(views.MethodView):
    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        form = ResetPwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            # 获取当前用户
            user = g.cms_user
            if user.check_password(oldpwd):
                # 密码验证通过，则修改密码
                user.password = newpwd
                db.session.commit()
                return restful.success()
            else:
                return restful.params_error(message='旧密码错误')
        else:
            # 当给Ajax返回数据时，要返回json格式的数据
            return restful.params_error(message=form.get_error())


class ResetEmailView(views.MethodView):
    def get(self):
        return render_template('cms/cms_resetemail.html')

    def post(self):
        pass


cms_bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
cms_bp.add_url_rule('/resetpwd/', view_func=ResetPwdView.as_view('resetpwd'))
cms_bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))
