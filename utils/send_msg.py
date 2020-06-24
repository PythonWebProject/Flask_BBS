from yunpian_python_sdk.model import constant as YC
from yunpian_python_sdk.ypclient import YunpianClient
from config import YP_API

def send_mobile_msg(mobile, code):
    # 初始化client,apikey作为所有请求的默认值
    clnt = YunpianClient(YP_API)
    param = {YC.MOBILE: mobile, YC.TEXT: '【Python进化讲堂】欢迎您注册熊熊论坛，验证码：{}（5分钟内有效，如非本人操作，请忽略）'.format(code)}
    r = clnt.sms().single_send(param)
    print(r.code(), r.msg(), r.data())
    return r.code()
