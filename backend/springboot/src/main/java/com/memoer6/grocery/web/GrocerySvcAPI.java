package com.memoer6.grocery.web;

import com.memoer6.grocery.model.Product;

import java.util.List;

public interface GrocerySvcAPI {

    //List products from catalog
    public List<Product> getProductsCatalog();

    //Add product to catalog
    public Product addProductCatalog(Product product);

    //Update product from catalog
    public void updateProductCatalog(Long productId, Product product);

    //Remove product from catalog
    public void removeProductCatalog(Long productId);

    //List products from shopping list
    public List<Product> getProductsShoppingList();

}
