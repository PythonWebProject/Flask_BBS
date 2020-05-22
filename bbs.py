'''
前台 front
后台 cms
公有 common
'''

from flask import Flask
from flask_wtf import CSRFProtect
from exts import db
from apps.cms.views import cms_bp
from apps.front.views import front_bp
import config


app = Flask(__name__)
CSRFProtect(app)
app.config.from_object(config)
app.config['TEMPLATE_AUTO_RELOAD'] = True
db.init_app(app)

app.register_blueprint(cms_bp)
app.register_blueprint(front_bp)


if __name__ == '__main__':
    app.run(debug=True)