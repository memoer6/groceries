
from flask import Flask


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



# Application factory
def create_app():

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
  app.config.from_object('config.default')
  # overrides the default configuration with values taken from the config.py file in the instance folder if
  # it exists. It contains configuration variables that contain sensitive information. The idea is to separate
  # these variables from those above and keep them out of the repository. You may be hiding secrets like database
  # passwords and API keys, or defining variables specific to a given machine. 
  app.config.from_pyfile('config.py', silent=True)
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
  app.config.from_envvar('APP_CONFIG_FILE', silent=True)

  # A Blueprint is a way to organize a group of related views and other code. Rather than registering views and
  # other code directly with an application, they are registered with a blueprint. Then the blueprint is
  # registered with the application when it is available in the factory function.
  from . import routes
  app.register_blueprint(routes.bp, url_prefix=app.config['URL_PREFIX'])

  # Initialize database
  from . import db 
  db.init_app(app)
  
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


