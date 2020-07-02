from flask import session, g
from .models import FrontUser
from .views import front_bp


@front_bp.before_request
def before_request():
    if 'user_id' in session:
        user_id = session.get('user_id')
        user = FrontUser.query.get(user_id)
        # 使用g对象保存用户
        if user:
            g.front_user = user