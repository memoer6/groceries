
import pytest
from urllib.parse import urljoin
import json

URL_PREFIX = 'api/v1/'

# Messages
PRODUCT_NAME_MISSING = "Field 'name' is required"
CREATE_DUPLICATED_PRODUCT = 'Product {} is already registered'
PRODUCT_NOT_FOUND = 'Product {} not found'
NO_PRODUCT_FIELDS_TO_UPDATE = 'No valid fields to update are detected'
NOT_BOOLEAN_TYPE = 'This value must be boolean'

# Class for pytest unit testing
class Product_test():
  def __init__(self, name=None, shopping_cart=False):
    self.name = name
    self.shopping_cart = shopping_cart

  def to_dict(self):    
    return self.__dict__


def get_products(client, query_params={}):
  # add query params to url if query_params dict is not empty
  url_path = 'products'
  if bool(query_params):
    for index, (param, value) in enumerate(query_params.items()):
      url_path += '?{}={},'.format(param, value)      
    url_path = url_path[:-1]  # remove last comma
  url = urljoin(URL_PREFIX, url_path)
  return client.get(url) 

def get_product_by_name(client, name=None):
  url = urljoin(URL_PREFIX, 'products/{}'.format(name))
  return client.get(url)  

def create_product(client, product):
  url = urljoin(URL_PREFIX, 'products')  
  # Passing the json argument in the test client methods sets the request data to the JSON-serialized object
  # and sets the content type to application/json. 
  return client.post(url, json=product) 

def delete_product(client, name=None):
  url = urljoin(URL_PREFIX, 'products/{}'.format(name))
  return client.delete(url)   

def update_product(client, product):
  url = urljoin(URL_PREFIX, 'products/{}'.format(product['name']))
  return client.put(url, json=product)


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
def test_get_products_with_one_product_in_db(client):
  bread = { 'name': 'bread'}
  create_product(client, bread)
  resp = get_products(client)
  assert resp.status_code == 200
  assert len(resp.get_json()) == 1 
  assert resp.get_json()[0]['name'] == 'bread'

"""
GIVEN the product database contains two products, one with 'shopping_cart' active and
      the other with 'shopping_cart' inactive
WHEN a request is sent to get products with query parameter 'shop' set to True 
THEN the response returns a list with only the product having 'shopping_cart' active and html code 200 (OK) 
"""
def test_get_products_with_shop_set_true(client):
  bread = { 'name': 'bread', 'shopping_cart': True}
  butter = { 'name': 'butter', 'shopping_cart': False}
  create_product(client, bread)
  create_product(client, butter)
  for value in ['true', 'True', 'TRUE']:
    resp = get_products(client, query_params={'shop': value})
    assert resp.status_code == 200
    assert len(resp.get_json()) == 1 
    assert resp.get_json()[0]['shopping_cart'] == True

"""
GIVEN the product database contains two products, one with 'shopping_cart' active and
      the other with 'shopping_cart' inactive
WHEN a request is sent to get products with query parameter 'shop' set to False 
THEN the response returns a list with all the products no matter the value of 'shopping_cart' 
      and html code 200 (OK) 
"""
def test_get_products_with_shop_set_false(client):
  bread = { 'name': 'bread', 'shopping_cart': True}
  butter = { 'name': 'butter', 'shopping_cart': False}
  create_product(client, bread)
  create_product(client, butter)
  for value in ['false', 'FALSE', 'False']:
    resp = get_products(client, query_params={'shop': value})
    assert resp.status_code == 200
    assert resp.get_json() == get_products(client).get_json() 

# GET PRODUCT BY NAME TESTS

"""
GIVEN the product database is empty 
WHEN a request is sent to get a product by name 
THEN the response returns an error message with html code 404 (Not Found)  
"""
def test_get_product_by_name_from_empty_db(client):
  resp = get_product_by_name(client, 'bread') 
  assert resp.status_code == 404  
  assert resp.get_json()['message'] == PRODUCT_NOT_FOUND.format('bread')


"""
GIVEN the product database has one product 
WHEN a request is sent to get that product by name 
THEN the response returns the product object with html code 200 (OK)  
"""
def test_get_product_by_name_with_that_product_in_db(client):
  bread = { 'name': 'bread'}
  create_product(client, bread)
  bread_model = Product_test('bread')
  resp = get_product_by_name(client, 'bread') 
  assert resp.status_code == 200
  assert resp.get_json() == bread_model.to_dict()

# CREATE PRODUCT TESTS

"""
GIVEN the product database is empty 
WHEN a request is sent to create a product with a name
THEN the response returns a product object with html code 201 (Created) 
"""
def test_create_product_from_empty_db(client):
  bread = { 'name': 'bread'}
  resp = create_product(client, bread)
  bread_model = Product_test('bread')
  assert resp.status_code == 201
  assert resp.get_json() == bread_model.to_dict()

"""
GIVEN the product database is empty 
WHEN a request is sent to create a product without json object in body
THEN the response returns an error message with html code 400 (Bad Request) 
"""
def test_create_product_without_body_payload(client):
  url = urljoin(URL_PREFIX, 'products')
  resp = client.post(url)
  assert resp.status_code == 400
  assert resp.get_json()['message']['name'] == PRODUCT_NAME_MISSING

"""
GIVEN the product database is empty 
WHEN a request is sent to create a product with json object not containing name property
THEN the response returns an error message with html code 400 (Bad Request) 
"""
def test_create_product_without_name_property(client):
  url = urljoin(URL_PREFIX, 'products')
  resp = client.post(url, json={'not_a_name': 'whatever'})
  assert resp.status_code == 400
  assert resp.get_json()['message']['name'] == PRODUCT_NAME_MISSING

"""
GIVEN the product database has one product 
WHEN a request is sent to create the same product  
THEN the response returns an error message with html code 400 (Bad Request) 
"""
def test_create_product_with_duplicate_name_in_db(client):
  bread = { 'name': 'bread'}
  create_product(client, bread)
  resp = create_product(client, bread)
  assert resp.status_code == 400  
  assert resp.get_json()['message'] == CREATE_DUPLICATED_PRODUCT.format('bread')

"""
GIVEN the product database is empty 
WHEN a request is sent to create a product with a field "shopping cart" not as a boolean  
THEN the response returns an error message with html code 400 (Bad Request) 
"""
def test_create_product_with_invalid_shopping_cart_type(client):
  bread = { 'name': 'bread', 'shopping_cart': 'a string' }
  resp = create_product(client, bread)
  assert resp.status_code == 400  
  assert resp.get_json()['message']['shopping_cart'] == NOT_BOOLEAN_TYPE

# DELETE PRODUCT TESTS

"""
GIVEN the product database has one product 
WHEN a request is sent to delete that product  
THEN the response returns a deleted message with html code 200(OK),
     and database becomes empty
"""
def test_delete_last_product_in_db(client):
  bread = { 'name': 'bread'}
  create_product(client, bread)
  delresp = delete_product(client, 'bread')
  getresp = get_products(client)
  assert delresp.status_code == 204  
  assert getresp.get_json() == [] 


"""
GIVEN the product database has one product 
WHEN a request is sent to delete another product  
THEN the response returns an error message with html code 404 (Not Found),
     and database remains with the original product
"""
def test_delete_product_with_nonexistent_name(client):
  bread = { 'name': 'bread'}
  create_product(client, bread)
  delresp = delete_product(client, 'butter')
  getresp = get_products(client)
  assert delresp.status_code == 404 
  assert delresp.get_json()['message'] == PRODUCT_NOT_FOUND.format('butter')
  assert len(getresp.get_json()) == 1 
  assert getresp.get_json()[0]['name'] == 'bread'


# UPDATE PRODUCT TESTS

"""
GIVEN the product database has one product 
WHEN a request is sent to update one mutable property of that product to a new value   
THEN the response returns the updated product with html code 200 (OK),
     and the property in that product changes to the new value
"""
def test_update_product_with_one_mutable_property(client):
  bread = { 'name': 'bread'}
  create_product(client, bread)
  bread['shopping_cart'] = True
  updresp = update_product(client, bread)
  getresp = get_product_by_name(client, 'bread')
  assert updresp.status_code == 200  
  assert updresp.get_json() == getresp.get_json()
  assert getresp.get_json()['shopping_cart'] == True 

"""
GIVEN the product database has one product 
WHEN a request is sent to update a product without json properties in body
THEN the response returns an error message with html code 400 (Bad Request) 
"""
def test_update_product_without_body_payload(client):
  bread = { 'name': 'bread'}
  create_product(client, bread)
  url = urljoin(URL_PREFIX, 'products/bread')
  resp = client.put(url)
  assert resp.status_code == 400
  assert resp.get_json()['message'] == NO_PRODUCT_FIELDS_TO_UPDATE


"""
GIVEN the product database has one product 
WHEN a request is sent to update one immutable property of that product to a new value   
THEN the response returns an error message with html code 400 (Bad Request),
    and the property in that product doesn't change to a new value 
"""
def test_update_product_with_one_immutable_property(client):
  bread = { 'name': 'bread'}
  create_product(client, bread) 
  bread['name'] = 'butter'
  updresp = update_product(client, bread)
  getresp = get_products(client)
  assert updresp.status_code == 400  
  assert updresp.get_json()['message'] == NO_PRODUCT_FIELDS_TO_UPDATE
  assert getresp.get_json()[0]['name'] == 'bread' 


"""
GIVEN the product database has one product 
WHEN a request is sent to update one nonexistent property of that product to a new value   
THEN the response returns an error message with html code 400 (Bad Request)
"""
def test_update_product_with_one_nonexistent_property(client):
  bread = { 'name': 'bread'}
  create_product(client, bread) 
  bread['nonexistent_field'] = 'whatever value'
  resp = update_product(client, bread)
  assert resp.status_code == 400  
  assert resp.get_json()['message'] == NO_PRODUCT_FIELDS_TO_UPDATE


"""
GIVEN the product database has one product 
WHEN a request is sent to update another product  
THEN the response returns an error message with html code 404 (Not Found)
"""
def test_update_product_with_nonexistent_name(client):
  bread = { 'name': 'bread'}
  create_product(client, bread)
  butter = { 'name': 'butter', 'shopping_cart': True}
  resp = update_product(client, butter)
  assert resp.status_code == 404  
  assert resp.get_json()['message'] == PRODUCT_NOT_FOUND.format('butter')

"""
GIVEN the product database has one product 
WHEN a request is sent to update the value of two properties of that product: one nonexistent 
     and one mutable  
THEN the response returns the updated product with html code 200 (OK) ignoring nonexistent properties
"""
def test_update_product_with_one_nonexistent_and_one_mutable_properties(client):
  bread = { 'name': 'bread'}
  create_product(client, bread) 
  bread['shopping_cart'] = True
  bread['nonexistent_field'] = 'whatever_value'
  resp = update_product(client, bread)
  assert resp.status_code == 200  
  assert resp.get_json()['shopping_cart'] == True
  assert 'nonexistent_field' not in resp.get_json()

"""
GIVEN the product database has one product 
WHEN a request is sent to update "shopping cart" field without a boolean value 
THEN the response returns an error message with html code 400 (Bad Request) 
"""
def test_update_product_with_invalid_shopping_cart_type(client):
  bread = { 'name': 'bread' }
  create_product(client, bread)
  bread['shopping_cart'] = 'a string'
  resp = update_product(client, bread)
  assert resp.status_code == 400  
  assert resp.get_json()['message']['shopping_cart'] == NOT_BOOLEAN_TYPE