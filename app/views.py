from flask import request
from flask import render_template, request

from app import pcb
from app.models import *

@pcb.route('/')
def home():
  return render_template('home.html')

@pcb.route('/register')
def register():
  if request.method == 'POST':
    pass
  return render_template('register.html')
