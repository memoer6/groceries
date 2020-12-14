from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

# The Flask-WTF extension uses Python classes to represent web forms. A form class simply defines the fields
# of the form as class variables.
# For each field, an object is created as a class variable in the ProductForm class. Each field is given a
# description or label as a first argument.
# The optional validators argument that you see in some of the fields is used to attach validation behaviors
# to fields. The DataRequired validator simply checks that the field is not submitted empty

class ProductForm(FlaskForm):
  name = StringField('Name: ', validators=[DataRequired(), Length(min=3, max=25)])
  shopping_cart = BooleanField('Shopping Cart: ')
