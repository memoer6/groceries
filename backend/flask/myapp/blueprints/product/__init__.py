from . import views, resources
from myapp.blueprints.product.resources import Product, ProductList, api


api.add_resource(resources.Product, '/products/<string:name>')
api.add_resource(resources.ProductList, '/products')    