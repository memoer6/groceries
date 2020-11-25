
from myapp.extensions import db
from myapp.database import Model


#SQL_ALquemy: The data that we will store in our database will be represented by a collection of classes that are
# referred to as the database models. The ORM layer will do the translations required to map objects
# created from these classes into rows in the proper database table.
#from flask import current_app

# The baseclass for all your models is called db.Model. It’s stored on the SQLAlchemy instance you have to create.
# Some parts that are required in SQLAlchemy are optional in Flask-SQLAlchemy. For instance the table name is
# automatically set for you unless overridden. It’s derived from the class name converted to lowercase and with
# “CamelCase” converted to “camel_case”. To override the table name, set the __tablename__ class attribute.
# Note how we never defined a __init__ method on the Product class? That’s because SQLAlchemy adds an implicit 
# constructor to all model classes which accepts keyword arguments for all its columns and relationships. If you
# decide to override the constructor for any reason, make sure to keep accepting **kwargs and call the super 
# constructor with those **kwargs to preserve this behavior
class Product(Model):
  ''' Model representing a product in the catalog '''

  __tablename__ = 'products'

  name = db.Column(db.String(50), primary_key=True)
  shopping_cart = db.Column(db.Boolean(), nullable=False)


  @staticmethod
  def find_all(filter=None): 
    ''' retrieve all products from the database matching the filter condition '''
    if filter is not None:
      products = Product.query.filter_by(**filter)      
    else:
      products = Product.query.all() 
    return Product.serialize_list(products)    

  @staticmethod
  def find_one(query=None):
    ''' retrieve a product from the database matching the query condition '''
    product = Product.query.filter_by(**query).first()
    if product is not None:
      product = product.serialize() 
    return product  

  @staticmethod
  def delete_one(query=None):
    product = Product.query.filter_by(**query).first()
    if product is not None:      
      return product.delete()
    return None  

  @staticmethod
  def update_one(query=None, props=None):
    product = Product.query.filter_by(**query).first()
    if product is not None:
      return product.update(**props) 
    return None   