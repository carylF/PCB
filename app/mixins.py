from datetime import datetime
from app import db
import bcrypt


class PersistenceMixin(object):
  '''
  Base model mixin to allow for new methods to be added for persistence.

  Methods:
    save(): Adds an object to the database. It simply
      serves to ensure that there is a clean seaparation
      between model and controller (view), and to present
      a clean API for data persistence.
    delete(): Removes an object from the database
    find(criteria): Finds an object by a criteria. Returns the object if it is found,
      or None if no user exists
    all(): Returns all objects in that table
  '''
  def save(self):
    db.session.add(self)
    db.session.commit()
    return self

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  @classmethod
  def find(cls, *args, **kwargs):
    return cls.query.filter(*args, **kwargs).first()

  @classmethod
  def find_all(cls, *args, **kwargs):
    return cls.query.filter(*args, **kwargs)

  @classmethod
  def create(cls, *args, **kwargs):
    instance = cls(*args, **kwargs)
    instance.save()
    return instance

  @classmethod
  def all(cls):
    return cls.query.all()


class SerializationMixin(object):
  '''
  Mixin to allow a class to be easily serialized to JSON
  Methods:
    serialize(): simplejson looks for this to serialize an object.
      This will allow for seamless serialization. The internal
      fix_encoding_issues function patches over any issues with
      json, such as date serialization
    serialize_all(query): Serializes all objects returned by a query
  '''
  def serialize(self):
    def fix_encoding_issues(obj):
      if isinstance(obj, datetime):
        return obj.isoformat()
      return obj
    result = dict()
    for key in self.__mapper__.c.keys():
      result[key] = fix_encoding_issues(getattr(self, key))
    return result

  @classmethod
  def serialize_query(cls, query):
    return [obj.serialize() for obj in query]

class PasswordMixin(object):
    '''
    Mixin with some convenience methods for password manaagement, namely
    hashing and comparing.
    Methods:
        hash(password, salt_length=10): Hashes a password with bcrypt, and default salt length of 10
        compare(password, hash): Compares a hash to a password using a constant time algorithm to
            prevent timing attacks.
    '''
    @staticmethod
    def hash_(password, salt_length=10):
        return bcrypt.hashpw(password, bcrypt.gensalt(salt_length))

    @staticmethod
    def compare(password, hash):
        return bcrypt.hashpw(password, hash) == hash
