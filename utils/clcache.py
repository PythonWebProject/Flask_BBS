import redis

# 连接Redis数据库
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


def save_captcha(key, value, timeout=300):
    '''把验证码存到Redis'''
    return r.set(key, value, timeout)


def get_captcha(key):
    '''从Redis中取验证码'''
    return r.get(key)


def delete_captcha(key):
    return r.delete(key)
