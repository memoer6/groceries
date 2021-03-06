
#A Flask application is an instance of the Flask class. Everything about the application, such as 
# configuration and URLs, will be registered with this class.

# Instead of creating a Flask instance globally, this creates it inside a function. 
# This function is known as the application factory. Any configuration, registration, and other setup the
#  application needs will happen inside the function, then the application will be returned.

# The __init__.py serves double duty: it will contain the application factory, and it tells Python that
# the myapp directory should be treated as a package.
# The Flask application object creation has to be in the __init__.py file. That way each module can import
# it safely and the __name__ variable will resolve to the correct package.
# All the view functions (the ones with a route() decorator on top) have to be imported in the __init__.py file.
# Import the view module after the application object is created.
from flask import Flask
from config import configs  
from myapp.blueprints import product
from myapp.extensions import (
  db,
  migrate
)


# Application factory
def create_app(env):

  # "__name__" is the name of the current Python module. The app needs to know where it’s located to set up
  # some paths, and __name__ is a convenient way to tell it that.
  # "instance_relative_config=True" tells the app that configuration files are relative to the instance folder.
  # The instance folder is located outside the myapp package and can hold local data that shouldn’t be committed
  # to version control, such as configuration secrets and the database file.
  # You can either explicitly provide the path of the instance folder when creating the Flask application or you
  # can let Flask autodetect the instance folder. For explicit configuration pass the "instance_path" parameter
  # If the "instance_path" parameter is not provided then the path "/instance" is used
  app = Flask(__name__, instance_relative_config=True)

  # preload the config from a module (module 'default' from package 'config'). You should not use this function 
  # to load the actual configuration but rather configuration defaults. The actual config should be loaded with
  # from_pyfile() and which is located outside myapp package because this package might be installed system wide 
  app.config.from_object(configs[env])
  
  # overrides the default configuration with values taken from the config.py file in the instance folder if
  # it exists. It contains configuration variables that contain sensitive information. The idea is to separate
  # these variables from those above and keep them out of the repository. You may be hiding secrets like database
  # passwords and API keys, or defining variables specific to a given machine. 
  # app.config.from_pyfile('config.py', silent=True)
 
  # Configuration based on environment variables:
  # Loads a configuration from an environment variable pointing to a configuration file.
  # The instance folder shouldn’t be in version control. This means that you won’t be able to track changes
  # to your instance configurations. That might not be a problem with one or two variables (in this case use your
  # instance folder to handle the configuration changes), but if you have finely tuned configurations for various
  # environments (production, staging, development, etc.) you don’t want to risk losing that.
  # Flask gives us the ability to choose a configuration file on load based on the value of an environment variable.
  # This means that we can have several configuration files in our repository and always load the right one
  # The value of the environment variable should be the absolute path to a configuration file.
  # silent – set to True if you want silent failure for missing files
  #app.config.from_envvar('APP_CONFIG_FILE', silent=True)

  register_extensions(app)
  register_blueprints(app)
  return app

# Configuration:
# The way Flask is designed usually requires the configuration to be available when the application starts up.
# Independent of how you load your config, there is a config object available which holds the loaded configuration 
# values: The config attribute of the Flask object. The config is actually a subclass of a dictionary and can be
# modified just like any dictionary
# Configuration from files:
# Configuration becomes more useful if you can store it in a separate file, ideally located outside the actual
# application package. This makes packaging and distributing your application possible via various package
# handling tools (Deploying with Setuptools) and finally modifying the configuration file afterwards.

def register_extensions(app):
  # Initialize database
  # It’s preferable to create your extensions and app factories so that the extension object does
  # not initially get bound to the application. Using this design pattern, no application-specific state is
  # stored on the extension object, so one extension object can be used for multiple apps.  
  # If you define your application in a function, but the SQLAlchemy object globally, how does the latter 
  # learn about the former? The answer is the init_app() function. What it does is prepare the application to
  #  work with SQLAlchemy. However that does not now bind the SQLAlchemy object to your application. 
  # Why doesn’t it do that? Because there might be more than one application created. So how does SQLAlchemy
  # come to know about your application? You will have to setup an application context.
  db.init_app(app)

  # The create_all() method to create the tables and database is not longer required inside the application factory
  # method because it's now handled by Flask-Migrate library by running "flask db init" command using Flask
  # command-line interface 
  #with app.app_context():
  #  db.create_all()

  # Flask-Migrate is an extension that handles SQLAlchemy database migrations for Flask applications
  # using Alembic. The database operations are made available through the Flask command-line interface or 
  # through the Flask-Script extension. The following example initializes the extension with the standard
  # Flask command-line interface. With the above application you can create the database or enable 
  # migrations if the database already exists with the following command: $ flask db init
  # This will add a migrations folder to your application. The contents of this folder need to be added to
  # version control along with your other source files. You can then generate an initial migration: $ flask db migrate
  # The migration script needs to be reviewed and edited, as Alembic currently does not detect every change you
  # make to your models. Then you can apply the migration to the database: $ flask db upgrade
  # Then each time the database models change repeat the migrate and upgrade commands.
  migrate.init_app(app, db)  

  return None

def register_blueprints(app):
  # A Blueprint is a way to organize a group of related views and other code. Rather than registering views and
  # other code directly with an application, they are registered with a blueprint. Then the blueprint is
  # registered with the application when it is available in the factory function.
  app.register_blueprint(product.views.bp)

  # Blueprint for groceries API
  app.register_blueprint(product.resources.api_bp, url_prefix=app.config['URL_PREFIX_API'])

  return None
