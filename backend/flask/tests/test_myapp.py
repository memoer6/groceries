# When we format the filename like test_*.py, it will be auto-discoverable by pytest.
# Pytest expects our tests to be located in files whose names begin with test_ or end with _test.py.

import os
import tempfile
import pytest
import json
from urllib.parse import urljoin
from myapp import create_app, db, models

# Error messages
INCORRECT_PRODUCT_JSON = 'Product name is required'
CREATE_DUPLICATED_PRODUCT = 'Product "{}" is already registered'
DELETE_PRODUCT_SUCCESSFULLY = 'Product "{}" was deleted successfully'
PRODUCT_NOT_FOUND = 'Product "{}" not found'
UPDATE_PRODUCT_SUCCESSFULLY = 'Product: "{}"\nFields updated: {}\nFields discarded: {}'
UPDATE_PRODUCT_WITHOUT_PROPS = 'No product fields are detected'
NO_PRODUCT_FIELDS_TO_UPDATE = 'The requested product field(s) cannot be updated'


# pytest fixture called client() that configures the application for testing and initializes a new database
# This client fixture will be called by each individual test. It gives us a simple interface to the application,
# where we can trigger test requests to the application.
@pytest.fixture
def client():
  '''
  Returns an empty sqlite3 database
  '''
  # Because SQLite3 is filesystem-based, we can easily use the tempfile module to create a temporary database
  # and initialize it. The mkstemp() function does two things for us: it returns a low-level file handle and
  # a random file name, the latter we use as database name. We just have to keep the db_fd around so that we
  # can use the os.close() function to close the file.
  app = create_app()
  db_fd, app.config['DATABASE'] = tempfile.mkstemp()
  # During setup, the TESTING config flag is activated. What this does is disable error catching during
  # request handling, so that you get better error reports when performing test requests against the application.
  app.config['TESTING'] = True
  global URL_PREFIX
  URL_PREFIX = app.config['URL_PREFIX']
  with app.test_client() as client:
      with app.app_context():
          db.init_db()
      yield client
  # To delete the database after the test, the fixture closes the file and removes it from the filesystem.
  os.close(db_fd)
  os.unlink(app.config['DATABASE'])

#def get_json(resp):
#  return json.loads(resp.data.decode('utf-8'))

def get_products(client, query_params={}):
  # add query params to url if query_params dict is not empty
  url_path = 'products'
  if bool(query_params):
    for index, (param, value) in enumerate(query_params.items()):
      url_path += '?{}={},'.format(param, value)      
    url_path = url_path[:-1]  # remove last comma
  url = urljoin(URL_PREFIX, url_path)
  return client.get(url) 

def create_product(client, name=None):
  url = urljoin(URL_PREFIX, 'products')
  # Passing the json argument in the test client methods sets the request data to the JSON-serialized object
  # and sets the content type to application/json. 
  json_data = {'name': name } 
  return client.post(url, json=json_data) 

def delete_product(client, name=None):
  url = urljoin(URL_PREFIX, 'products/{}'.format(name))
  return client.delete(url)   

def update_product(client, name=None, props={}):
  url = urljoin(URL_PREFIX, 'products/{}'.format(name))
  return client.put(url, json=props)

# GET PRODUCT TESTS

"""
GIVEN the product database is empty 
WHEN a request is sent to get products 
THEN the response returns an empty list with html code 200 (OK)  
"""
def test_empty_db(client):
  resp = get_products(client) 
  assert resp.status_code == 200
  # You can get the JSON data from the request or response with get_json.
  assert resp.get_json() == [] 

"""
GIVEN the product database contains one product 
WHEN a request is sent to get products 
THEN the response returns a list with one product object and html code 200 (OK) 
"""
def test_get_products_with_one_prodcut_in_db(client):
  create_product(client, 'bread')
  resp = get_products(client)
  assert resp.status_code == 200
  assert len(resp.get_json()) == 1 

"""
GIVEN the product database contains two products, one with 'shoppingCart' active and
      the other with 'shoppingCart' inactive
WHEN a request is sent to get products with query parameter 'shop' set to True 
THEN the response returns a list with only the product having 'shoppingCart' active and html code 200 (OK) 
"""
def test_get_products_with_shop_set_true(client):
  create_product(client, 'bread')
  create_product(client, 'butter')
  update_product(client, 'bread', props={'shoppingCart': 1})
  bread = models.Product('bread', shopping_cart=1)
  resp = get_products(client, query_params={'shop': 'true'})
  assert resp.status_code == 200
  assert len(resp.get_json()) == 1 
  assert resp.get_json()[0] == bread.to_dict()

# TODO Include test sending 'shop' set to False

# CREATE PRODUCT TESTS

"""
GIVEN the product database is empty 
WHEN a request is sent to create a product with a name
THEN the response returns a product object with html code 201 (Created) 
"""
def test_create_product_from_empty_db(client):
  resp = create_product(client, 'bread')
  bread = models.Product('bread')
  assert resp.status_code == 201
  assert resp.get_json() == bread.to_dict()

"""
GIVEN the product database is empty 
WHEN a request is sent to create a product without json object in body
THEN the response returns an error message with html code 400 (Bad Request) 
"""
def test_create_product_without_body_payload(client):
  url = urljoin(URL_PREFIX, 'products')
  resp = client.post(url)
  assert resp.status_code == 400
  assert resp.data.decode('utf-8') == INCORRECT_PRODUCT_JSON

"""
GIVEN the product database is empty 
WHEN a request is sent to create a product with json object not containing name property
THEN the response returns an error message with html code 400 (Bad Request) 
"""
def test_create_product_without_name_property(client):
  url = urljoin(URL_PREFIX, 'products')
  resp = client.post(url, json={'not_a_name': 'whatever'})
  assert resp.status_code == 400
  assert resp.data.decode('utf-8') == INCORRECT_PRODUCT_JSON

"""
GIVEN the product database has one product 
WHEN a request is sent to create the same product  
THEN the response returns an error message with html code 400 (Bad Request) 
"""
def test_create_product_with_duplicate_name_in_db(client):
  create_product(client, 'bread')
  resp = create_product(client, 'bread')
  assert resp.status_code == 400  
  assert resp.data.decode('utf-8') == CREATE_DUPLICATED_PRODUCT.format('bread')

# DELETE PRODUCT TESTS

"""
GIVEN the product database has one product 
WHEN a request is sent to delete that product  
THEN the response returns a deleted message with html code 200(OK),
     and database becomes empty
"""
def test_delete_last_product_in_db(client):
  create_product(client, 'bread')
  delresp = delete_product(client, 'bread')
  getresp = get_products(client)
  assert delresp.status_code == 200  
  assert delresp.data.decode('utf-8') == DELETE_PRODUCT_SUCCESSFULLY.format('bread')
  assert getresp.get_json() == [] 


"""
GIVEN the product database has one product 
WHEN a request is sent to delete another product  
THEN the response returns an error message with html code 404 (Not Found),
     and database remains with one product
"""
def test_delete_product_with_nonexistent_name(client):
  create_product(client, 'bread')
  delresp = delete_product(client, 'butter')
  getresp = get_products(client)
  assert delresp.status_code == 404  
  assert delresp.data.decode('utf-8') == PRODUCT_NOT_FOUND.format('butter')
  assert len(getresp.get_json()) == 1 


# UPDATE PRODUCT TESTS

"""
GIVEN the product database has one product 
WHEN a request is sent to update one mutable property of that product to a new value   
THEN the response returns an updated message with html code 200 (OK),
     and the property in that product changes to the new value
"""
def test_update_product_with_one_mutable_property(client):
  create_product(client, 'bread')
  updresp = update_product(client, 'bread', props={'shoppingCart': 1})
  getresp = get_products(client)
  assert updresp.status_code == 200  
  assert updresp.data.decode('utf-8') == \
                UPDATE_PRODUCT_SUCCESSFULLY.format('bread', '"shoppingCart"', '')
  assert getresp.get_json()[0]['shoppingCart'] == 1 

"""
GIVEN the product database has one product 
WHEN a request is sent to update a product without json properties in body
THEN the response returns an error message with html code 400 (Bad Request) 
"""
def test_update_product_without_body_payload(client):
  create_product(client, 'bread')
  url = urljoin(URL_PREFIX, 'products/bread')
  resp = client.put(url)
  assert resp.status_code == 400
  assert resp.data.decode('utf-8') == UPDATE_PRODUCT_WITHOUT_PROPS


"""
GIVEN the product database has one product 
WHEN a request is sent to update one immutable property of that product to a new value   
THEN the response returns an error message with html code 400 (Bad Request),
    and the property in that product doesn't change to a new value 
"""
def test_update_product_with_one_immutable_property(client):
  create_product(client, 'bread')  
  updresp = update_product(client, 'bread', props={'name': 'butter'})
  getresp = get_products(client)
  assert updresp.status_code == 400  
  assert updresp.data.decode('utf-8') == NO_PRODUCT_FIELDS_TO_UPDATE
  assert getresp.get_json()[0]['name'] == 'bread' 


"""
GIVEN the product database has one product 
WHEN a request is sent to update one nonexistent property of that product to a new value   
THEN the response returns an error message with html code 400 (Bad Request)
"""
def test_update_product_with_one_nonexistent_property(client):
  create_product(client, 'bread')  
  resp = update_product(client, 'bread', props={'nonexistent_field': 'whatever_value'})
  assert resp.status_code == 400  
  assert resp.data.decode('utf-8') == NO_PRODUCT_FIELDS_TO_UPDATE


"""
GIVEN the product database has one product 
WHEN a request is sent to update another product  
THEN the response returns an error message with html code 404 (Not Found)
"""
def test_update_product_with_nonexistent_name(client):
  create_product(client, 'bread')
  resp = update_product(client, 'butter', props={'shoppingCart': 1})
  assert resp.status_code == 404  
  assert resp.data.decode('utf-8') == PRODUCT_NOT_FOUND.format('butter')

"""
GIVEN the product database has one product 
WHEN a request is sent to update the value of two properties of that product: one nonexistent 
     and one mutable  
THEN the response returns an update message with html code 200 (OK) indicating the property 
     that was updated
"""
def test_update_product_with_one_nonexistent_and_one_mutable_properties(client):
  create_product(client, 'bread')  
  props = {
    'shoppingCart': 1,
    'nonexistent_field': 'whatever_value'
  }
  resp = update_product(client, 'bread', props=props)
  assert resp.status_code == 200  
  assert resp.data.decode('utf-8') == \
          UPDATE_PRODUCT_SUCCESSFULLY.format('bread', '"shoppingCart"', '"nonexistent_field"')
