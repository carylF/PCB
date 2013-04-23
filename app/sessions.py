from functools import wraps

from flask import redirect, url_for, flash
from werkzeug.contrib.cache import SimpleCache
from flask import session
import os

from app.models import User

class _UserSessions(object):
  def __init__(self):
    self.cache = SimpleCache()

  def create(self, user_id):
    if User.find(User.id == user_id) is None:
      return None
    sess = os.urandom(24)
    self.cache.set(sess, user_id)
    session['key'] = sess
    return sess

  def get(self):
    if 'key' not in session:
      return None
    key = session['key']
    user_id = self.cache.get(key)
    user = User.find(User.id == user_id)
    return user

  def delete(self):
    if 'key' in session:
      self.cache.delete(session['key'])
      session.pop('key', None)


sessions = _UserSessions()

def login_required(f):
  @wraps(f)
  def decorated_view(*args, **kwargs):
    if sessions is not None and sessions.get() is None:
      return redirect(url_for('login'))
    return f(*args, **kwargs)
  return decorated_view

def guest_required(f):
  @wraps(f)
  def decorated_view(*args, **kwargs):
    if sessions is not None and sessions.get() is None:
      return f(*args, **kwargs)
    flash(u'You are already logged in', 'error')
    return redirect(url_for('home'))
  return decorated_view
