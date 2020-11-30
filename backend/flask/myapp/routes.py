
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

from flask import request, make_response, Blueprint, current_app
from myapp.database import db
from myapp.models.product import Product
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
    filter = { 'shopping_cart': True } if shop else None
    products = Product.find_all(filter) 
  except Exception as e:
    current_app.logger.error(e.args) 
    return make_response('Cannot complete the operation', 500) 
  
  # return response
  return make_response(json.dumps(products), 200, {'Content-Type': 'application/json'} )


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
  try:
    product = Product.create(name=name, shopping_cart=False)
  except Exception as e:
    current_app.logger.error(e.args[0])
    if 'sqlite3.IntegrityError' in e.args[0] or 'psycopg2.errors.UniqueViolation' in e.args[0]: 
      return make_response('Product "{}" is already registered'.format(name) , 400) 
    else:
      return make_response('Cannot complete the operation', 500)      
  current_app.logger.info('Product "{}" was saved in database'.format(name))
  # Return product  
  return make_response(json.dumps(product) , 201, {'Content-Type': 'application/json'})
      

@bp.route('/products/<name>', methods = ['GET'])
def get_product_by_name(name): 
  '''
  Return the product by the given name
  ''' 
  current_app.logger.info('Request to retrieve data of product "{}" from the catalog'.format(name))

  # Check if product is registered 
  try:
    query = { 'name': name }
    product = Product.find_one(query)
  except Exception as e:
    current_app.logger.error(e.args)
    return make_response('Cannot complete the operation', 500) 

  if product is None:
    current_app.logger.info('Product "{}" not found'.format(name))
    return make_response('Product "{}" not found'.format(name), 404)
  
  # Return product
  return make_response(json.dumps(product), 200, {'Content-Type': 'application/json'})


@bp.route('/products/<name>', methods = ['DELETE']) 
def delete_product(name):
  '''
  Delete a product from the catalog
  :param name: name of the product to delete  
  '''
  current_app.logger.info('Request to delete product "{}" from the catalog'.format(name))

  # Delete product into database 
  try:
    query = { 'name': name }
    result = Product.delete_one(query)
  except Exception as e:
    current_app.logger.error(e.args)
    return make_response('Cannot complete the operation', 500) 

  # Product wasn't registered
  if result is None:
    current_app.logger.info('Product "{}" not found'.format(name))
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
  props = {prop:value for (prop,value) in data_json.items() if prop in mutable_properties}

  # No property to update
  if not bool(props):
    return make_response('The requested product field(s) cannot be updated', 400)   
  
  # Update product in database  
  try:
    query = { 'name': name }
    result = Product.update_one(query, props)
  except Exception as e:
    current_app.logger.error(e.args)  
    return make_response('Cannot complete the operation', 500) 

  if result is None:
    current_app.logger.info('Product "{}" not found'.format(name))
    return make_response('Product "{}" not found'.format(name), 404)  
    
  # Return response
  updated_props = ','.join([ '"{}"'.format(k) for k,v in props.items()])
  message = 'Product: "{}"\nFields updated: {}'.format(name, updated_props)
  return make_response(message , 200)
  