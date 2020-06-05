import random


def get_random_captcha(num):
    '''生成随机验证码'''
    code = ''
    for i in range(num):
        num = str(random.randint(0, 9))
        upper = chr(random.randint(65, 90))
        lower = chr(random.randint(97, 122))
        lst = [num, upper, lower]
        ret = random.choice(lst)
        code = ''.join([code, ret])
    return code