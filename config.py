import os

# 数据库连接配置
HOSTNAME = '127.0.0.1'
PORT = 3306
USERNAME = 'root'
PASSWORD = 'root'
DATABASE = 'flask_bbs'
DB_URL = 'mysql+mysqlconnector://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

TEMPLATE_AUTO_RELOAD = True
SQLALCHEMY_DATABASE_URI = DB_URL
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_RECYCLE = 280
SQLALCHEMY_POOL_SIZE = 20

# 设置密钥
SECRET_KEY = os.urandom(15)

# 发送邮箱服务地址
MAIL_SERVER = 'smtp.qq.com'
# 邮箱端口，为587或465，为587时TLS设置为True，为465时SSL设置为True
MAIL_PORT = 587
MAIL_USE_TLS = True
# MAIL_USE_SSL = True # MAIL_PORT为465时设置此项
# 用户名可以为你的邮箱，需要自行添加
MAIL_USERNAME = '379869029@qq.com'
# 邮箱密码，不是邮箱账号密码，而是第三方客户端登录使用的授权码，需要自行获取
MAIL_PASSWORD = 'vrxiqciwjnbcxxxx'
# 发送者即你的邮箱，需要自行添加
MAIL_DEFAULT_SENDER = '379869029@qq.com'

# 云片APIKEY
YP_API = 'edf71361381f31b3957beda37f20xxxx'

# 七牛云存储配置
QINIU_ACCESS_KEY = '_PL7p4sTSlfAKl71hIkuG3F6y18681ZKkNJ3xxxx'
QINIU_SECRET_KEY = '4P09jodUqhhEqIOcaqT9daVFmKjCJI3l6gsAxxxx'
QINIU_BUCKET_NAME = 'bbs-images'
QINIU_BUCKET_DOMAIN = 'qcquuxxxx.bkt.clouddn.com'

# 分页配置
PER_PAGE = 10
CMS_PER_PAGE = 15

# celery配置项
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'