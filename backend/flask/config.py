from os.path import dirname, abspath, join

basedir = abspath(dirname(__file__))


class Config:
  # API service setting
  URL_PREFIX='/v1/'

  # Groccery list application settings
  MUTABLE_PRODUCT_PROPERTIES=['shopping_cart']

  #Database settings with FLASK SQLALCHEMY 
  #By using the exact naming conventions for the variables above, simply having them in our config file will
  # automatically configure our database connections for us. We will never have to create engines, sessions,
  # or connections.
  SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(basedir, 'myapp.db')
  # When set to 'True', Flask-SQLAlchemy will log all database activity to Python's stderr for debugging purposes.
  SQLALCHEMY_ECHO = False 
  #If set to True, Flask-SQLAlchemy will track modifications of objects and emit signals. The default is None,
  # which enables tracking but issues a warning that it will be disabled by default in the future. This requires
  # extra memory and should be disabled if not needed.
  SQLALCHEMY_TRACK_MODIFICATIONS = False

