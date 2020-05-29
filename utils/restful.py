from flask import jsonify


class HttpCode(object):
    ok = 200
    unauth = 401
    paramerror = 400
    server = 500


def restful_result(code, message, data):
    return jsonify({'code': code, 'message': message, 'data': data})


def success(message='', data=None):
    return restful_result(code=HttpCode.ok, message=message, data=data)


def unauth_error(message=""):
    return restful_result(code=HttpCode.unauth, message=message, data=None)


def params_error(message=""):
    return restful_result(code=HttpCode.paramerror, message=message, data=None)


def server_error(message=""):
    return restful_result(code=HttpCode.paramerror, message=message or '服务器内部错误', data=None)