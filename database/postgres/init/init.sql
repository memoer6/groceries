

-- PostgreSQL
-- The prevalent convention for column name is lower_case_with_underscores 

CREATE TABLE IF NOT EXISTS products (
  name VARCHAR(50) PRIMARY KEY,
  shopping_cart BOOLEAN 
);
