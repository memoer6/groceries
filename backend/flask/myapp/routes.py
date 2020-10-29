
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
from . import db

#Instantiate blueprint 
bp = Blueprint('grocery_list', __name__)

   
@bp.route('/products', methods = ['GET'])
def get_products(): 
  '''
  Return the list of all products in the catalog
  ''' 
  current_app.logger.info('Request to retrieve all products in the catalog')
  shop = request.args.get('shop', False)

  # Get product list from database
  sql = 'SELECT * FROM products'
  products = db.query_db(sql)

  # If query parameter "shop" is True, then only list products to buy in grocery store (shoppingCart = True)
  if shop:
    return make_response(jsonify(
      [ product for product in products if product['shoppingCart'] == True ]),
      200
    )
  return make_response(jsonify(products) , 200)



@bp.route('/products', methods = ['POST']) 
def create_product():
  '''
  Create a new product into the catalog
  '''
  current_app.logger.info('Request to create product into the catalog')
  # Parses the incoming JSON request data and returns it
  # silent – if set to True this method will fail silently and return None  
  data_json = request.get_json(silent=True)
  
  # Check that json object is included in payload
  if data_json is None:
    return make_response('Product name is required' , 400)  

  # Check that name attribute is included in json object  
  name = data_json.get('name', None)
  if name is None:
    return make_response('Product name is required' , 400)
  
  # Check that product is not already registered
  # 'one' argument is like fetchone(): returns one row from the query. If the query returned no results, it returns None
  # db.execute takes a SQL query with ? placeholders for any user input, and a tuple of values to replace the
  # placeholders with. The database library will take care of escaping the values so you are not vulnerable to
  # a SQL injection attack.
  product = db.query_db('SELECT name FROM products WHERE name = ?', args=(name,), one=True)  
  if product is not None:
    return make_response('Product "{}" is already registered'.format(name) , 400)

  # Create product into database   
  sql = 'INSERT INTO products (name, shoppingCart) VALUES (?, ?)'
  args = (data_json['name'], False)
  rowid = db.run_db(sql, args)
  current_app.logger.info('Record {} was created'.format(rowid))

  # Return product
  product = db.query_db('SELECT * FROM products WHERE name = ?', args=(name,), one=True)
  return make_response(jsonify(product) , 201)
      


@bp.route('/products/<name>', methods = ['DELETE']) 
def delete_product(name):
  '''
  Delete a product from the catalog
  :param name: name of the product to delete  
  '''
  current_app.logger.info('Request to delete product "{}" from the catalog'.format(name))

  # Check if product is registered
  product = db.query_db('SELECT name FROM products WHERE name = ?', args=(name,), one=True)
  if product is None:
    return make_response('Product "{}" not found'.format(name), 404)

  # Delete product into database   
  db.run_db('DELETE FROM products WHERE name = ?', args=(name,))
  current_app.logger.info('Record {} was deleted'.format(name))

  # Return response
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
  
  # Check if product is registered
  product = db.query_db('SELECT name FROM products WHERE name = ?', args=(name,), one=True)
  if product is None:
    return make_response('Product "{}" not found'.format(name), 404)

  # Extract the properties to update and properties to discard
  mutable_properties = current_app.config['MUTABLE_PRODUCT_PROPERTIES']
  accepted_properties, discarded_properties = [], []
  for prop in data_json.items():
    if prop[0] in mutable_properties:
      accepted_properties.append(prop)
    else:
      discarded_properties.append(prop)  

  # No property to update
  if len(accepted_properties) == 0:
    return make_response('The requested product field(s) cannot be updated', 400)

  # Build SQL statement to update product
  # column_placeholders represents the set of column names to set with ? placeholders for the SQL update statement
  column_names = ''
  # column_values represents the values of the placeholder for the SQL update statement
  column_values = []
  for (prop_name, value) in accepted_properties:
    column_names += '{} = ?,'.format(prop_name) 
    column_values.append(value)
  column_names = column_names[:-1] #remove last comma
  column_values.append(name) # include name for SQL condition (WHERE) 
  sql = 'UPDATE products SET {} WHERE name = ?'.format(column_names) 

  # Update product in database  
  current_app.logger.info('Update SQL statement: {}'.format(sql))
  db.run_db(sql, args=tuple(column_values))

  # Return response
  updated_props = ','.join([ '"{}"'.format(k) for k,v in accepted_properties])
  discarded_props = ','.join([ '"{}"'.format(k) for k,v in discarded_properties])
  message = 'Product: "{}"\nFields updated: {}\nFields discarded: {}'.format(name, updated_props, discarded_props)
  return make_response(message , 200)
  