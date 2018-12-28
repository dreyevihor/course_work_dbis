from flask import session, redirect
from functools import wraps

__all__=('login_required',)


def login_required(func, url='/login/'):
    @wraps(func)
    def wrap(*args, **kwargs):
        if 'user_pk' in session:
            return func(*args, **kwargs)
        else:
            return redirect(url)
    return wrap
