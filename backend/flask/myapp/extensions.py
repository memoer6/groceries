"""Extensions module. Each extension is initialized in the app factory located in app.py."""

from flask_sqlalchemy import SQLAlchemy

  
# This extension provides a wrapper for the SQLAlchemy project, which is an Object Relational Mapper or ORM.
# ORMs allow database applications to work with objects instead of tables and SQL. The operations performed
# on the objects are translated into database commands transparently by the ORM.
#from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
