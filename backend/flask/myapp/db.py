
import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext


# The application will use a SQLite database to store products. Python comes with built-in support for SQLite 
# in the sqlite3 module.

# This is a helper function that store database connection safely on the g object. The first time the function
# is called, it will create a database connection for the current context, and successive calls will return the
# already established connection
def get_db():
  # g is a special object that is unique for each request. It is used to store data that might be accessed by 
  # multiple functions during the request. The connection is stored and reused instead of creating a new
  # connection if get_db is called a second time in the same request.
  if not hasattr(g, 'db'):
    # sqlite3.connect() establishes a connection to the file pointed at by the DATABASE configuration key.
    # This file doesn’t have to exist yet, and won’t until you initialize the database later.
    g.db = sqlite3.connect(
      # current_app is another special object that points to the Flask application handling the request. 
      # Since you used an application factory, there is no application object when writing the rest of your
      # code. get_db will be called when the application has been created and is handling a request, so 
      # current_app can be used.
      current_app.config['DATABASE'],
      detect_types=sqlite3.PARSE_DECLTYPES
    )
    # To simplify working with SQLite, a row factory function is useful. It is executed for every result
    # returned from the database to convert the result. 
    # This would use Row objects to return the results of queries. These are namedtuples, so we can access them
    # either by index or by key.   
    #g.db.row_factory = sqlite3.Row
    g.db.row_factory = make_dicts
  return g.db

# For instance, in order to get dictionaries instead of tuples, this could be inserted into the get_db
# function we created above
def make_dicts(cursor, row):
  return dict((cursor.description[idx][0], value) for idx, value in enumerate(row))

# close_db checks if a connection was created by checking if g.sqlite_db was set. If the connection exists, 
# it is closed. Further down you will tell your application about the close_db function in the application 
# factory so that it is called after each request.
def close_db(error):
  if hasattr(g, 'db'):
    g.db.close()


# Initializes the database
def init_db():
  db = get_db()
  # The open_resource() method of the application object is a convenient helper function that will open a
  # resource that the application provides. This function opens a file from the resource location 
  # and allows you to read from it. It is used in this example to execute a script on the database 
  # connection.
  # The connection object provided by SQLite can give you a cursor object. On that cursor, there is a
  # method to execute a complete script. 
  with current_app.open_resource('schema.sql') as f:
    db.executescript(f.read().decode('utf8'))
  # Finally, you only have to commit the changes. SQLite3 and other transactional databases will not commit
  # unless you explicitly tell it to.  
  db.commit()

# The close_db and init_db_command functions need to be registered with the application instance; otherwise,
# they won’t be used by the application. However, since you’re using a factory function, that instance isn’t
# available when writing the functions. Instead, write a function that takes an application and does the 
# registration. This function is call from __init__
def init_app(app):
  # app.teardown_appcontext() tells Flask to call that function when cleaning up after returning the response.
  app.teardown_appcontext(close_db)
  # app.cli.add_command() adds a new command that can be called with the flask command.
  app.cli.add_command(init_db_command)     

# The click.command() decorator registers a new command with the flask script (flask init-db). When the command
# executes, Flask will automatically create an application context which is bound to the right application. 
# Within the function, you can then access flask.g and other things as you might expect. When the script ends, 
# the application context tears down and the database connection is released.
@click.command('init-db')
@with_appcontext
def init_db_command():
  init_db()
  click.echo('Initialized the database.')   

# Provide a query function that combines getting the cursor, executing and fetching the results
def query_db(query, args=(), one=False):
  # create a Cursor object by calling the cursor method of the Connection object
  cursor = get_db().execute(query, args)
  resp = cursor.fetchall()
  cursor.close()
  # if resp contains records, return the first if one=True or all if one=False. Return None if resp doesn't
  # contain records
  return (resp[0] if resp else None) if one else resp

# Function to run expression that create, update or delete a record in database
def run_db(sql, args=()):
  # connect to the SQLite database by creating a Connection object.
  conn = get_db()  
  cursor = conn.execute(sql, args)
  # Since this query modifies data, db.commit() needs to be called afterwards to save the changes.
  conn.commit()
  return cursor.lastrowid

