from flask import Blueprint, render_template, views, request, redirect, url_for, session, g
from flask_mail import Message
from sqlalchemy import or_

from apps.cms.forms import LoginForm, ResetPwdForm, ResetEmailForm, AddBannerForm, UpdateBannerForm, AddBoardForm, UpdateBoardForm
from apps.cms.models import CMSUser, CMSPermission, BannerModel, BoardModel
from exts import db, mail
from utils import restful, random_captcha, clcache
from .decorators import permission_required  # .代表当前路径

cms_bp = Blueprint('cms', __name__, url_prefix='/cms')

from .hooks import before_request

@cms_bp.route('/')
# @login_required
def index():
    return render_template('cms/cms_index.html', max_role=g.max_role)


@cms_bp.route('/logout/')
def logout():
    # 清空session
    del session['user_id']
    # 重定向到登录页面
    return redirect(url_for('cms.login'))


@cms_bp.route("/profile/")
def profile():
    return render_template("cms/cms_profile.html", max_role=g.max_role)


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
        return render_template('cms/cms_resetpwd.html', max_role=g.max_role)

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
        return render_template('cms/cms_resetemail.html', max_role=g.max_role)

    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            # 修改用户邮箱
            g.cms_user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())


class EmailCaptchaView(views.MethodView):
    def get(self):
        email = request.args.get('email')
        if not email:
            return restful.params_error('请传递邮箱参数')
        # 发送邮件验证码，可以是4位或6位的数字与英文组合
        captcha = random_captcha.get_random_captcha(4)
        try:
            message = Message('熊熊论坛验证码', recipients=[email], body='您正在进行更改邮箱验证，验证码是%s，5分钟内有效，请及时输入、注意保密。' % captcha)
            mail.send(message)
        except Exception as e:
            print(e.args[0])
            return restful.server_error('邮件发送异常，请检查重试')
        clcache.save_captcha(email, captcha)
        return restful.success(message='邮件发送成功，请注意接收验证码')


@cms_bp.route('/posts/')
@permission_required(CMSPermission.POSTER)
def posts():
    return render_template('cms/cms_posts.html', max_role=g.max_role)


@cms_bp.route('/banners/')
@permission_required(CMSPermission.BANNER)
def banners():
    banners = BannerModel.query.filter(or_(BannerModel.is_delete == 0, BannerModel.is_delete == None)).order_by(BannerModel.priority.desc()).all()
    return render_template('cms/cms_banners.html', max_role=g.max_role, banners=banners)


@cms_bp.route('/abanner/', methods=['POST'])
@permission_required(CMSPermission.BANNER)
def abanner():
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel(name=name, image_url=image_url, link_url=link_url, priority=priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


@cms_bp.route('/ubanner/', methods=['POST'])
@permission_required(CMSPermission.BANNER)
def ubanner():
    # 根据id修改数据
    form = UpdateBannerForm(request.form)
    if form.validate():
        banner_id = form.banner_id.data
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel.query.get(banner_id)
        if banner and banner.is_delete != 1:
            banner.name = name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='轮播图不存在')
    else:
        return restful.params_error(form.get_error())


@cms_bp.route('/dbanner/', methods=['POST'])
@permission_required(CMSPermission.BANNER)
def dbanner():
    banner_id = request.form.get('banner_id')
    if not banner_id:
        return restful.params_error(message='数据请求有误')
    banner = BannerModel.query.get(banner_id)
    if banner and banner.is_delete != 1:
        banner.is_delete = 1
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message='轮播图不存在')


@cms_bp.route('/comments/')
@permission_required(CMSPermission.COMMENTER)
def comments():
    return render_template('cms/cms_comments.html', max_role=g.max_role)


@cms_bp.route('/boards/')
@permission_required(CMSPermission.BOARDER)
def boards():
    boards = BoardModel.query.filter(or_(BoardModel.is_delete == 0, BoardModel.is_delete == None)).all()
    return render_template('cms/cms_boards.html', max_role=g.max_role, boards=boards)


@cms_bp.route('/aboard/', methods=['POST'])
@permission_required(CMSPermission.BOARDER)
def aboard():
    form = AddBoardForm(request.form)
    if form.validate():
        name = form.name.data
        board = BoardModel(name=name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    else:
        restful.params_error(message=form.get_error())


@cms_bp.route('/uboard/', methods=['POST'])
@permission_required(CMSPermission.BOARDER)
def uboard():
    form = UpdateBoardForm(request.form)
    if form.validate():
        board_id = form.board_id.data
        name = form.name.data
        board = BoardModel.query.get(board_id)
        if board and board.is_delete != 1:
            board.name = name
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有该板块')
    else:
        return restful.params_error(form.get_error())


@cms_bp.route('/dboard/', methods=['POST'])
@permission_required(CMSPermission.BOARDER)
def dboard():
    board_id = request.form.get('board_id')
    if not board_id:
        return restful.params_error(message='板块不存在')
    board = BoardModel.query.get(board_id)
    if board and board.is_delete != 1:
        board.is_delete = 1
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message='板块不存在')


@cms_bp.route('/fusers/')
@permission_required(CMSPermission.FRONTUSER)
def fusers():
    return render_template('cms/cms_fusers.html', max_role=g.max_role)


@cms_bp.route('/cusers/')
@permission_required(CMSPermission.CMSUSER)
def cusers():
    return render_template('cms/cms_cusers.html', max_role=g.max_role)


@cms_bp.route('/croles/')
@permission_required(CMSPermission.ADMINER)
def croles():
    return render_template('cms/cms_croles.html', max_role=g.max_role)


cms_bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
cms_bp.add_url_rule('/resetpwd/', view_func=ResetPwdView.as_view('resetpwd'))
cms_bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))
cms_bp.add_url_rule('/email_captcha/', view_func=EmailCaptchaView.as_view('email_captcha'))
