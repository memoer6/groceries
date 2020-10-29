-- In SQLite, data is stored in tables and columns. These need to be created before you can store and retrieve 
-- data. myapp will store products in the products table. Create a file with the SQL commands needed to 
-- create empty tables

DROP TABLE IF EXISTS products;

CREATE TABLE products (
  name TEXT PRIMARY KEY,
  shoppingCart BOOLEAN 
);

