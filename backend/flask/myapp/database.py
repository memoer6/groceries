
"""Database module, including the SQLAlchemy database object and DB-related utilities."""

from myapp.extensions import db
from sqlalchemy.inspection import inspect
from flask import current_app


# Serialization mixin. The serialization function basically fetches all attributes the SQLAlchemy inspector
# exposes and puts it in a dict.
class Serializer(object):

  def serialize(self):
    return {prop: getattr(self, prop) for prop in inspect(self).attrs.keys()}

  @staticmethod
  def serialize_list(l):
    return [m.serialize() for m in l]


#SQL_ALquemy: The data that we will store in our database will be represented by a collection of classes that are
# referred to as the database models. The ORM layer will do the translations required to map objects
# created from these classes into rows in the proper database table.
#from flask import current_app

# The baseclass for all your models is called db.Model. It’s stored on the SQLAlchemy instance you have to create.
# Some parts that are required in SQLAlchemy are optional in Flask-SQLAlchemy. For instance the table name is
# automatically set for you unless overridden. It’s derived from the class name converted to lowercase and with
# “CamelCase” converted to “camel_case”. To override the table name, set the __tablename__ class attribute.
# Note how we never defined a __init__ method on the User class? That’s because SQLAlchemy adds an implicit 
# constructor to all model classes which accepts keyword arguments for all its columns and relationships. If you
# decide to override the constructor for any reason, make sure to keep accepting **kwargs and call the super 
# constructor with those **kwargs to preserve this behavior
class Product(db.Model, Serializer):
  ''' Model representing a product in the catalog '''
  name = db.Column(db.String(50), primary_key=True)
  shopping_cart = db.Column(db.Boolean(), nullable=False)

# The __repr__ method tells Python how to print objects of this class. We will use this for debugging.
  def __repr__(self):
    return '<Product {}>'.format(name)




