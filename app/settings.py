import os

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')

SECRET_KEY = '{4XDW9r:i*)M5bE!ODlJi,v8-[boI|Di+-@TyP3k^)OsH+qqo8]=|JUvsaavC5+'
