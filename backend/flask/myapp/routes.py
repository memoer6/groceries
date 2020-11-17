
# The Flask application object has attributes, such as config, that are useful to access within views and CLI
# commands. However, importing the app instance within the modules in your project is prone to circular import
# issues. When using the app factory pattern or writing reusable blueprints or extensions there won’t be an app
# instance to import at all.
# Flask solves this issue with the application context. Rather than referring to an app directly, you use the
# current_app proxy, which points to the application handling the current activity.
# Lifetime of the context: The application context is created and destroyed as necessary. When a Flask 
# application begins handling a request, it pushes an application context and a request context. When the
# request ends it pops the request context then the application context. Typically, an application context
# will have the same lifetime as a request.

from flask import jsonify, request, make_response, Blueprint, current_app
#from . import sqlite3_db as db
from myapp.database import db, Product
import traceback
import json

#Instantiate blueprint 
bp = Blueprint('grocery_list', __name__)


@bp.route('/products', methods = ['GET'])
def get_products(): 
  '''
  Return the list of all products in the catalog
  ''' 
  current_app.logger.info('Request to retrieve all products in the catalog')
  shop = request.args.get('shop', 'false')
  shop = (shop.lower() == 'true')

  # If query parameter "shop" is True, then only list products to buy in grocery store (shopping_cart = True)
  try:
    products = Product.query.filter_by(shopping_cart=True) if shop else Product.query.all()
  except Exception as e:
    current_app.logger.error(e.args)  
  
  # return response
  return make_response(json.dumps(Product.serialize_list(products)), 200, {'Content-Type': 'application/json'} )

@bp.route('/products', methods = ['POST']) 
def create_product():
  '''
  Create a new product into the catalog
  '''
  current_app.logger.info('Request to create product into the catalog')
  # Parses the incoming JSON request data and returns it
  # silent – if set to True this method will fail silently and return None  
  data_json = request.get_json(silent=True)
  
  # Check that json object is included in payload or "name" attribute is included in json object
  if data_json is None or data_json.get('name', None) is None:
    return make_response('Product name is required' , 400)  
  name = data_json.get('name')

  # Create product into database  
  product = Product(name=name, shopping_cart=False)
  try:
    db.session.add(product)
    db.session.commit()
  except Exception as e:
    current_app.logger.error(e.args)
    if 'sqlite3.IntegrityError' in e.args[0]: 
      return make_response('Product "{}" is already registered'.format(name) , 400)    
  current_app.logger.info('Product "{}" was saved in database'.format(name))
  # Return product  
  return make_response(json.dumps(product.serialize()) , 201, {'Content-Type': 'application/json'})
      

@bp.route('/products/<name>', methods = ['GET'])
def get_product_by_name(name): 
  '''
  Return the product by the given name
  ''' 
  current_app.logger.info('Request to retrieve data of product "{}" from the catalog'.format(name))

  # Check if product is registered 
  try:
    product = Product.query.filter_by(name=name).first()
  except Exception as e:
    current_app.logger.error(e.args)

  if product is None:
    return make_response('Product "{}" not found'.format(name), 404)
  
  # Return product
  return make_response(json.dumps(product.serialize()), 200, {'Content-Type': 'application/json'})


@bp.route('/products/<name>', methods = ['DELETE']) 
def delete_product(name):
  '''
  Delete a product from the catalog
  :param name: name of the product to delete  
  '''
  current_app.logger.info('Request to delete product "{}" from the catalog'.format(name))

  # Delete product into database 
  try:
    result = Product.query.filter_by(name=name).delete()
    db.session.commit()
  except Exception as e:
    current_app.logger.error(e.args)

  # Product wasn't registered
  if result == 0:
    return make_response('Product "{}" not found'.format(name), 404)
  
  # Product was deleted successfully
  current_app.logger.info('Record {} was deleted'.format(name))
  return make_response('Product "{}" was deleted successfully'.format(name) , 200)

 

@bp.route('/products/<name>', methods = ['PUT'])
def update_product(name):
  '''
  Update a product from the catalog
  :param name: name of the product to update 
  '''
  current_app.logger.info('Request to update product "{}" from the catalog'.format(name))

  # Check that json object is included in payload
  data_json = request.get_json(silent=True)
  if data_json is None:
    return make_response('No product fields are detected' , 400)   

  # Extract the properties to update and properties to discard
  mutable_properties = current_app.config['MUTABLE_PRODUCT_PROPERTIES']
  properties_to_update = [prop for prop in data_json.items() if prop[0] in mutable_properties]

  # No property to update
  if len(properties_to_update) == 0:
    return make_response('The requested product field(s) cannot be updated', 400)   
  
  # Check if product is registered
  try:
    product = Product.query.filter_by(name=name).first()
  except Exception as e:
    current_app.logger.error(e.args)

  if product is None:
    return make_response('Product "{}" not found'.format(name), 404)
  
  # Update product in database    
  for prop in properties_to_update:
    key, value = prop
    setattr(product, key, value)

  try:
    db.session.commit()  
  except Exception as e:
    current_app.logger.error(e.args)  
    
  # Return response
  updated_props = ','.join([ '"{}"'.format(k) for k,v in properties_to_update])
  message = 'Product: "{}"\nFields updated: {}'.format(name, updated_props)
  return make_response(message , 200)
  