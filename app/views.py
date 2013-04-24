from flask import render_template, request, flash, redirect, url_for
from app.sessions import sessions, login_required, guest_required
from werkzeug import secure_filename
import os

from app import pcb
from app.models import *

@pcb.route('/')
def home():
  return render_template('home.html')

@pcb.route('/computer')
def computer():
  return render_template('computer.html')

@pcb.route('/login', methods=['GET', 'POST'])
@guest_required
def login():
  if request.method == 'POST':
    user = User.authenticate(**request.form.to_dict())
    if user is None:
      flash(u'No user with those credentials found.', 'error')
      return redirect(url_for('login'))
    sessions.create(user.id)
    flash(u'Login successful', 'success')
    return redirect(url_for('dashboard'))
  return render_template('login.html')

@pcb.route('/register', methods=['GET', 'POST'])
@guest_required
def register():
  if request.method == 'POST':
    u = request.form.to_dict()
    u.pop('cpwd', None)
    user = User.create(**u)
    sessions.create(user.id)
    flash(u'Registration successful', 'success')
    return redirect(url_for('dashboard'))
  return render_template('register.html')

@pcb.route('/logout')
@login_required
def logout():
  sessions.delete()
  flash(u'Logged out successfully', 'success')
  return redirect(url_for('home'))

@pcb.route('/build')
@login_required
def build():
  parts = Part.all()
  return render_template('add_build.html', parts=parts)

@pcb.route('/dashboard')
@login_required
def dashboard():
  return render_template('dashboard.html')

@pcb.route('/dashboard/add')
@login_required
def add():
  return render_template('add_build.html')

@pcb.route('/dashboard/add_part', methods=['GET', 'POST'])
@login_required
def add_part():
  if request.method == 'POST':
    print request.form, request.files
    photo = request.files['photo']
    if photo is not None:
      filename = os.path.join(pcb.config['UPLOAD_FOLDER'], secure_filename(photo.filename))
      photo.save(filename)
      p = request.form.to_dict(flat=True)
      p['photo'] = filename
      part = Part.create(**p)
      flash('Part saved successfully', 'success')
      return redirect(url_for('dashboard'))
    flash(u'No file given', 'error')
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

@pcb.route('/dashboard/select_build')
@login_required
def select():
  if request.method == 'POST':
    pass
  return render_template('select_build.html')

@pcb.route('/dashboard/view_orders')
@login_required
def view_orders():
  orders = Build.find_all(Build.seller_id == sessions.get().id)
  total = reduce(lambda x, y: x+y, (order.total for order in orders), 0)
  return render_template('view_orders.html', orders=orders)

@pcb.route('/dump')
def dump():
  from flask import Response
  users = User.all()
  print g.user
  return Response((str(user) for user in users))
