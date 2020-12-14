
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

from flask import Blueprint, render_template, abort, request, redirect, flash, url_for
from myapp.blueprints.product.models import Product as ProductDao
from myapp.blueprints.product.forms import ProductForm

#Instantiate blueprint 
bp = Blueprint('products', __name__, url_prefix='/products')


@bp.route('/')
def list():
  products = ProductDao.find_all()
  return render_template('list.html', title='Products', products=products, description='Products Catalog')  

# Any view using FlaskForm to process the request is already getting CSRF protection
@bp.route('/create/', methods = ['GET', 'POST'])
def create():
  form = ProductForm()
  if form.validate_on_submit():
    flash('Product {} has been created'.format(form.name.data))
    # delete csrf_token field from product because is not supported in the product model
    del form['csrf_token']
    ProductDao.create(**form.data)
    return redirect(url_for('products.list'))
  return render_template('create.html', title='Create', form=form) 

@bp.route('/shop/')
def shop():
  filter = { 'shopping_cart': True }
  products = ProductDao.find_all(filter)
  return render_template('list.html', title='Shop', products=products, description='Shopping Cart')   