from flask import render_template, request, flash
from app.sessions import sessions, login_required, guest_required
from werkzeug import secure_filename
import os

from app import pcb
from app.models import *

@pcb.route('/')
def home():
  return render_template('home.html')

@pcb.route('/login', methods=['GET', 'POST'])
@guest_required
def login():
  if request.method == 'POST':
    user = User.authenticate(**request.form)
    if user is None:
      flash(u'No user with those credentials found.', 'error')
      return render_template('login.html')
    sessions.create(user.id)
    return redirect(url_for('dashboard'))
  return render_template('login.html')

@pcb.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    u = request.post.to_dict()
    u.pop('conpasswd', None)
    user = User.create(**u)
    sessions.create(user.id)
    return redirect(url_for('dashboard'))
  return render_template('register.html')

@pcb.route('/dashboard')
@login_required
def dashboard():
  return render_template('dashboard.html')

@pcb.route('/dashboard/add')
@login_required
def add_build():
  if request.method == 'POST':
    build = Build(**request.form)
  return render_template('add_build.html')

@pcb.route('/dashboard/add_part')
@login_required
def add_part():
  if request.method == 'POST':
    photo = request.files['photo']
    if photo is not None:
      filename = os.path.join(pcb.config['UPLOAD_FOLDER'], secure_filename(photo.filename))
      photo.save(filename)
      p = request.form.to_dict(flat=True)
      p['photo'] = filename
      part = Part.create(**p)
      flash('Part saved successfully')
      return redirect(url_for('dashboard'))
    else:
      flash(u'No file given')
      return redirect(url_for('add_part'))
  return render_template('add_part.html')


@pcb.route('/dashboard/edit')
@login_required
def edit_build():
  pass

@pcb.route('/dashboard/history')
@login_required
def history():
  return render_template('history.html')
