from __future__ import print_function

import functools

from flask import session, redirect, url_for, request


def loginRequired(function):
    @functools.wraps(function)
    def inner(*args, **kwargs):
        if session.get('logged_in'):
            return function(*args, **kwargs)
        return redirect(url_for('login', next=request.path))

    return inner
