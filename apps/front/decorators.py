from flask import session, redirect, url_for, g

def login_required(func):
    def inner(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('front.signin'))
    return inner