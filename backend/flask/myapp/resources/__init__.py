
from flask import Blueprint
from flask_restful import Api
from myapp.resources.product import Product, ProductList


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(Product, '/products/<string:name>')
api.add_resource(ProductList, '/products')




