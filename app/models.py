from pcbuilder import db
from mixins import PersistenceMixin, SerializationMixin, PasswordMixin

class BaseModelMixin(PersistenceMixin, SerializationMixin):
  '''
  Hold all the mixins every model shares to reduce typing.
  Really just a lazy man's class.
  '''
  pass

class User(db.Model, BaseModelMixin, PasswordMixin):
  id = db.Column(db.Integer, primary_key=True)
  email_address = db.Column(db.String)
  password = db.Column(db.String)
  first_name = db.Column(db.String)
  last_name = db.Column(db.String)

  def __init__(self, email_address, password, first_name, last_name):
    self.email_address = email_address
    self.password = hash_(password)
    self.first_name = first_name
    self.last_name = last_name

  def __repr__(self):
    return '%s %s' % (self.first_name, self.last_name)

  def authenticate(self, email_address, password):
    user = User.find(User.email_address == email_address)
    if user and compare(password, user.password):
      return user
    return None

class Part(db.Model, BaseModelMixin):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  photo = db.Column(db.String)
  price = db.Column(db.String)

  def __init__(self, name, photo, price):
    self.name = name
    self.photo = photo
    self.price = price

  def __repr__(self):
    return self.name

class Build(db.Model, BaseModelMixin):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String)
  buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  seller_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  buyer = db.relationship('User', backref=db.backref('purchases', dynamic=True))
  seller = db.relationship('User', backref=db.backref('sales', dynamic=True))

  def __init__(self, title, buyer, seller):
    self.title = title
    self.buyer = buyer
    self.seller = seller

  def __repr__(self):
    return self.title


class Transaction(db.Model, BaseModelMixin):
  id = db.Column(db.Integer, primary_key=True)
  part_id = db.Column(db.Integer, db.ForeignKey('part.id'))
  build_id = db.Column(db.Integer, db.ForeignKey('build.id'))

  part = db.relationship('Part')
  build = db.relationship('Build', backref=db.backref('transactions', dynamic=True))

  def __init__(self, part, build):
    self.part = part
    self.build = build

  def __repr__(self):
    return self.part.name

