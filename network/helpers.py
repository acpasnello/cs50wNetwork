import os
import urllib.parse
from random import randrange

from functools import wraps
from .models import User, Post, Like


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id') is None:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

def get_likes(posts, userid):
    liked = {}
    for post in posts:
        # check if user has liked each post
        getlikes = Like.objects.filter(post=post).filter(user_id=userid).count()
        if getlikes > 0:
            liked[post.pk] = True
        else:
            liked[post.pk] = False

    return liked
