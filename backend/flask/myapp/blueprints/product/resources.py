
from flask_restful import Resource, fields, marshal_with, abort, reqparse, inputs, Api
from flask import current_app, Blueprint
from myapp.blueprints.product.models import Product as ProductDao


api_bp = Blueprint('api', __name__)
api = Api(api_bp)


# Output fields
# Flask-RESTful provides an easy way to control what data you actually render in your response. With the fields
# module, you can use whatever objects (ORM models/custom classes/etc.) you want in your resource. fields also
# lets you format and filter the response so you don’t have to worry about exposing internal data structures.

product_fields = {
  'name': fields.String,
  'shopping_cart': fields.Boolean
}

# Request Parsing
# While Flask provides easy access to request data (i.e. querystring or POST form encoded data), it’s still a
# pain to validate form data. Flask-RESTful has built-in support for request data validation using a
# library similar to argparse.
# The whole request parser part of Flask-RESTful is slated for removal and will be replaced by documentation
# on how to integrate with other packages that do the input/output stuff better
# Using the reqparse module also gives you sane error messages for free. If an argument fails to pass
# validation, Flask-RESTful will respond with a 400 Bad Request and a response highlighting the error.
# Calling parse_args with strict=True ensures that an error is thrown if the request includes arguments
# your parser does not define:  args = parser.parse_args(strict=True)
# If you specify the help value, it will be rendered as the error message when a type error is raised while
# parsing it. If you do not specify a help message, the default behavior is to return the message from the
# type error itself.
# By default, arguments are not required. Also, arguments supplied in the request that are not part of the
# RequestParser will be ignored. Arguments declared in your request parser but not set in the request itself
# will default to None.
# To require a value be passed for an argument, just add required=True to the call to add_argument().
# By default, the RequestParser tries to parse values from flask.Request.values, and flask.Request.json.
# Use the location argument to add_argument() to specify alternate locations to pull the values from. 
# Any variable on the flask.Request can be used.
# The default way errors are handled by the RequestParser is to abort on the first error that occurred.
# This can be beneficial when you have arguments that might take some time to process. However, often it
# is nice to have the errors bundled together and sent back to the client all at once. This behavior can
# be specified either at the Flask application level or on the specific RequestParser instance. To invoke
# a RequestParser with the bundling errors option, pass in the argument bundle_errors.

product_list_parser = reqparse.RequestParser()
product_list_parser.add_argument('shop', type=inputs.boolean, help='This value must be boolean',\
                                    location='args', default=False)

create_product_parser = reqparse.RequestParser(bundle_errors=True)
create_product_parser.add_argument('name', required=True, help="Field 'name' is required")  
create_product_parser.add_argument('shopping_cart', type=inputs.boolean, help='This value must be boolean',\
                                             default=False)                               

update_product_parser = reqparse.RequestParser(bundle_errors=True)
# store_missing– Whether the arguments default value should be stored if the argument is missing from the request.
update_product_parser.add_argument('shopping_cart', type=inputs.boolean, help='This value must be boolean',\
                                          store_missing=False)

# The main building block provided by Flask-RESTful are resources. Resources are built on top of Flask 
# pluggable views, giving you easy access to multiple HTTP methods just by defining methods on your resource. 
# The decorator marshal_with is what actually takes your data object and applies the field filtering. The
# marshalling can work on single objects, dicts, or lists of objects.
# An optional envelope keyword argument is specified to wrap the resulting output.

class Product(Resource):
 
  @marshal_with(product_fields)
  def get(self, name):
    '''
    Retrieve a product by name from the catalog
    :param name: name of the product to update 
    '''
    current_app.logger.info('Request to retrieve data of product "{}" from the catalog'.format(name))
    # Check if product is registered 
    try:
      query = { 'name': name }
      product = ProductDao.find_one(query)
    except Exception as e:
      current_app.logger.error(e.args)
      abort(500, message='Cannot complete the operation')  
    if product is None:
      current_app.logger.info('Product "{}" not found'.format(name))
      abort(404, message="Product {} not found".format(name)) 
    return product  

  def delete(self, name):
    ''' 
    Delete a product from the catalog
    :param name: name of the product to delete  
    '''
    current_app.logger.info('Request to delete product "{}" from the catalog'.format(name))
    # Delete product into database 
    try:
      query = { 'name': name }
      result = ProductDao.delete_one(query)
    except Exception as e:
      current_app.logger.error(e.args)
      abort(500, message='Cannot complete the operation')
    # Product wasn't registered
    if result is None:
      current_app.logger.info('Product "{}" not found'.format(name))
      abort(404, message="Product {} not found".format(name))     
    # Product was deleted successfully
    current_app.logger.info('Record {} was deleted'.format(name))
    return '', 204

  def put(self, name):
    '''
    Update a product from the catalog
    :param name: name of the product to update 
    '''
    current_app.logger.info('Request to update product "{}" from the catalog'.format(name))
    # Validate input arguments    
    args = update_product_parser.parse_args()
    if not args:
      abort(400, message='No valid fields to update are detected')   
    args['name'] = name       
    # Update product in database  
    try:
      query = { 'name': name }
      result = ProductDao.update_one(query, args)
    except Exception as e:
      current_app.logger.error(e.args)  
      abort(500, message='Cannot complete the operation') 
    if result is None:
      current_app.logger.info('Product "{}" not found'.format(name))
      abort(404, message="Product {} not found".format(name))      
    # Return product
    return self.get(name)  

  

class ProductList(Resource):
  @marshal_with(product_fields)
  def get(self):
    ''' Return the list of all products in the catalog  ''' 
    current_app.logger.info('Request to retrieve all products in the catalog')
    # Validate input arguments
    args = product_list_parser.parse_args()
    # If query parameter "shop" is True, then only list products to buy in grocery store (shopping_cart = True)
    try:
      filter = { 'shopping_cart': True } if args['shop'] == True else None
      products = ProductDao.find_all(filter) 
    except Exception as e:
      current_app.logger.error(e.args) 
      abort(500, message='Cannot complete the operation')      
    return products, 200

  def post(self):
    ''' Create a new product into the catalog '''    
    current_app.logger.info('Request to create product into the catalog')
    # Validate input arguments
    args = create_product_parser.parse_args()
    name = args['name'] 
    # Create product into database  
    try:
      product = ProductDao.create(**args)
    except Exception as e:
      current_app.logger.error(e.args[0])
      if 'sqlite3.IntegrityError' in e.args[0] or 'psycopg2.errors.UniqueViolation' in e.args[0]: 
        abort(400, message='Product {} is already registered'.format(name))       
      else:
        abort(500, message='Cannot complete the operation')      
    current_app.logger.info('Product "{}" was saved in database'.format(name))
    # Return product  
    return product, 201  

