


class Product():
  def __init__(self, name=None, shopping_cart=0):
    self.name = name
    self.shoppingCart = shopping_cart

  def to_dict(self):    
    return self.__dict__  
