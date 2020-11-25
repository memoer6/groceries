
"""Database module, including the SQLAlchemy database object and DB-related utilities."""

from myapp.extensions import db
from sqlalchemy.inspection import inspect


# Serialization mixin. The serialization function basically fetches all attributes the SQLAlchemy inspector
# exposes and puts it in a dict. Another option could be to implement marshmallow library
class Serializer(object):

  def serialize(self):
    return {prop: getattr(self, prop) for prop in inspect(self).attrs.keys()}

  # Static methods, much like class methods, are methods that are bound to a class rather than its object.
  # They are not dependent on the state of the object. Static method knows nothing about the class and just
  # deals with the parameters  
  @staticmethod
  def serialize_list(l):
    return [m.serialize() for m in l]


class CRUDMixin(Serializer):
  """ Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

  # Returns a class method for the given function. A class method is a method that is bound to a class rather
  # than its object. It doesn't require creation of a class instance, much like @staticmethod.
  # Unlike @staticmethod, Class method works with the class since its parameter is always the class itself.
  @classmethod
  def create(cls, **kwargs):
    """Create a new record and save it the database."""
    instance = cls(**kwargs)
    return instance.save().serialize()

  def update(self, commit=True, **kwargs):
    """Update specific fields of a record."""
    for attr, value in kwargs.items():
      setattr(self, attr, value)
    return commit and self.save() or self

  def save(self, commit=True):
    """Save the record."""
    db.session.add(self)
    if commit:
      db.session.commit()
    return self

  def delete(self, commit=True):
    """Remove the record from the database."""
    db.session.delete(self)
    if commit:
      db.session.commit()
    return self


class Model(CRUDMixin, db.Model):
  """Base model class that includes CRUD convenience methods."""

  __abstract__ = True


