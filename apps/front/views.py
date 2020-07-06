from flask import Blueprint, views, render_template, make_response, request, session, g, redirect, url_for
from flask_paginate import Pagination, get_page_parameter
from io import BytesIO
from sqlalchemy import or_
from sqlalchemy.sql import func

from utils.captcha import Captcha
from utils import clcache, restful, safe_url
from .forms import SignupForm, SigninForm, AddPostForm, AddCommentForm
from .models import FrontUser, PostModel, CommentModel, PraiseModel
from .decorators import login_required
from apps.cms.models import BannerModel, BoardModel, HighlightPostModel
from exts import db
import config

front_bp = Blueprint('front', __name__)

from .hooks import before_request


@front_bp.route('/')
def index():
    banners = BannerModel.query.filter(or_(BannerModel.is_delete == 0, BannerModel.is_delete == None)).order_by(
        BannerModel.priority.desc()).limit(4)
    boards = BoardModel.query.filter(or_(BoardModel.is_delete == 0, BoardModel.is_delete == None)).all()
    board_id = request.args.get('board_id', type=int, default=None)
    # 当前页
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * config.PER_PAGE
    end = start + config.PER_PAGE
    sort = request.args.get('st', type=int, default=1)
    query_obj = PostModel.query.filter(or_(PostModel.is_delete == 0, PostModel.is_delete == None))
    # 最新文章
    if sort == 1:
        query_obj = query_obj.order_by(PostModel.create_time.desc())
    # 精华帖
    elif sort == 2:
        query_obj = db.session.query(PostModel).join(HighlightPostModel).order_by(HighlightPostModel.create_time.desc()).filter(or_(PostModel.is_delete == 0, PostModel.is_delete == None))
    # 点赞最多
    elif sort == 3:
        query_obj = query_obj.order_by(PostModel.like_count.desc())
    # 评论最多
    elif sort == 4:
        query_obj = db.session.query(PostModel).join(CommentModel).filter(or_(PostModel.is_delete == 0, PostModel.is_delete == None)).group_by(PostModel.id).order_by(func.count(CommentModel.id).desc())

    if board_id:
        query_obj = query_obj.filter(PostModel.board_id==board_id)
        posts = query_obj.slice(start, end)
        total = query_obj.count()
    else:
        posts = query_obj.slice(start, end)
        total = query_obj.count()
    request_arg = request.args.get('board_id')
    if request_arg:
        show_all = False
    else:
        show_all = True

    pagination = Pagination(page=page, total=total, bs_version=3, per_page=config.PER_PAGE)
    context = {
        'banners': banners,
        'boards': boards,
        'current_board': board_id,
        'posts': posts,
        'show_all': show_all,
        'pagination': pagination,
        'current_sort': sort
    }
    return render_template('front/front_index.html', **context)


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


@front_bp.route('/acomment/', methods=['POST'])
@login_required
def add_comment():
    form = AddCommentForm(request.form)
    if form.validate():
        content = form.content.data
        post_id = form.post_id.data
        post = PostModel.query.get(post_id)
        if post and post.id != 1:
            comment = CommentModel(content=content)
            comment.post = post
            comment.commenter = g.front_user
            db.session.add(comment)
            post.comment_count += 1
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='该文章去火星啦😀')
    else:
        return restful.params_error(message=form.get_error())


class PostView(views.MethodView):
    decorators = [login_required]

    def get(self):
        boards = BoardModel.query.filter(or_(BoardModel.is_delete == 0, BoardModel.is_delete == None)).all()
        return render_template('front/front_apost.html', boards=boards)

    def post(self):
        form = AddPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            board = BoardModel.query.get(board_id)
            if board and board.is_delete != 1:
                post = PostModel(title=title, content=content)
                post.board = board
                post.author = g.front_user
                db.session.add(post)
                db.session.commit()
                # return redirect(url_for('front.index'))
                return restful.success()
            else:
                return restful.params_error(message='没有该板块，请重新选择')
        else:
            return restful.params_error(form.get_error())


@front_bp.route('/p/<post_id>/')
def post_detail(post_id):
    post = PostModel.query.get(post_id)
    if post and post.is_delete != 1:
        # 阅读数增加
        post.read_count += 1
        db.session.commit()
        if hasattr(g, 'front_user'):
            praise = PraiseModel.query.filter_by(post_id=post_id).filter_by(praiser_id=g.front_user.id).first()
            if praise:
                return render_template('front/front_pdetail.html', post=post, praise=1)
        return render_template('front/front_pdetail.html', post=post, praise=0)
    else:
        return restful.params_error(message='文章不存在')


@front_bp.route('/praise/', methods=['POST'])
def praise():
    if hasattr(g, 'front_user'):
        is_praise = request.form.get('is_praised', type=int, default=0)
        post_id = request.form.get('post_id', type=int, default=None)
        post = PostModel.query.get(post_id)
        if post and post.is_delete != 1:
            print('isd: ', is_praise)
            if is_praise:
                post.like_count -= 1
                praise = PraiseModel.query.filter_by(post_id=post_id).filter_by(praiser_id=g.front_user.id).first()
                db.session.delete(praise)
                db.session.commit()
            else:
                post.like_count += 1
                praise = PraiseModel(post_id=post_id, praiser_id=g.front_user.id)
                db.session.add(praise)
                db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='文章不存在')
    else:
        return redirect(url_for('front.signin'))


class SignupView(views.MethodView):
    def get(self):
        # referrer表示页面的跳转，即从哪个页面跳转到当前页面
        print('Referer:', request.referrer)
        return_to = request.referrer
        # is_safe_url()判断请求是否来自站内
        if return_to and return_to != request.url and safe_url.is_safe_url(return_to):
            return render_template('front/front_signup.html', return_to=return_to)
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
front_bp.add_url_rule('/apost/', view_func=PostView.as_view('apost'))
