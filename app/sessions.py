from functools import wraps

from flask import redirect, url_for, flash
from werkzeug.contrib.cache import SimpleCache
from flask import sessions
import os

from app.models import User

class _UserSessions(object):
  def __init__(self):
    self.cache = SimpleCache()

  def create(self, user_id):
    if User.find(User.id == user_id) is None:
      return None
    sess = os.urandom(24)
    self.cache = self.cache.set(sess, user_id)
    session['key'] = sess
    return sess

  def get(self, key):
    user_id = self.cache.get(sess)
    user = User.find(User.id == user_id)
    return user


sessions = _UserSessions()

def login_required(f):
  @wraps(f)
  def decorated_view(*args, **kwargs):
    if not 'key' in session and sessions.get(session['key']) is None:
      return redirect(url_for('login'))
    return f(*args, **kwargs)
  return decorated_view

def guest_required(f):
  @wraps(f)
  def decorated_view(*args, **kwargs):
    if not 'key' in session and sessions.get(session['key']) is None:
      return f(*args, **kwargs)
    flash(u'You are already logged in', 'error')
    return redirect(url_for('home'))
  return decorated_view
