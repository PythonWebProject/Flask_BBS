from flask import Blueprint, render_template, views

cms_bp = Blueprint('cms', __name__, url_prefix='/cms')

@cms_bp.route('/')
def index():
    return '后台管理首页'


class LoginView(views.MethodView):
    def get(self):
        return render_template('cms/cms_login.html')


cms_bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))