import os
# environs is a Python library for parsing environment variables. It allows you to store configuration
# separate from your code. Read .env files into os.environ (useful for local development)
from environs import Env


env = Env()
# By default, Env.read_env will look for a .env file in current directory and (if no .env exists in the CWD)
# recurse upwards until a .env file is found
env.read_env()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
  # API service setting
  URL_PREFIX_API='/api/v1/'
  
  # When set to 'True', Flask-SQLAlchemy will log all database activity to Python's stderr for debugging purposes.
  SQLALCHEMY_ECHO = False 
  #If set to True, Flask-SQLAlchemy will track modifications of objects and emit signals. The default is None,
  # which enables tracking but issues a warning that it will be disabled by default in the future. This requires
  # extra memory and should be disabled if not needed.
  SQLALCHEMY_TRACK_MODIFICATIONS = False

  # Flask Form
  # CSRF protection requires a secret key to securely sign the token. By default this will use the 
  # Flask app's SECRET_KEY. If you'd like to use a separate token you can set WTF_CSRF_SECRET_KEY.
  SECRET_KEY = os.urandom(32)
  # You can disable CSRF protection in all views by default, by setting WTF_CSRF_CHECK_DEFAULT to False,
  # and selectively call protect() only when you need
  # WTF_CSRF_CHECK_DEFAULT = False

class DevConfig(Config):
  #Database settings with FLASK SQLALCHEMY 
  #By using the exact naming conventions for the variables above, simply having them in our config file will
  # automatically configure our database connections for us. We will never have to create engines, sessions,
  # or connections.
  SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'myapp.db')
  #SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
 
class TestConfig(Config):
  SQLALCHEMY_DATABASE_URI = env.str('TEST_DATABASE_URI')
  # TESTING = True

class ProdConfig(Config):
  pass

configs = {
  'dev'  : DevConfig,
  'test' : TestConfig,
  'prod' : ProdConfig,
  'default' : ProdConfig
  }    
