package com.memoer6.grocery.web;

//HTTP requests are handled by a controller. These components are easily identified by the @RestController annotation,
//and the UserController below handles GET requests

//Spring 4.0 introduced @RestController, a specialized version of the controller which is a convenience annotation
//that does nothing more than add the @Controller and @ResponseBody annotations. By annotating the controller class
//with @RestController annotation, you no longer need to add @ResponseBody to all the request mapping methods.
//The @ResponseBody annotation is active by default

//The key difference between a human-facing controller and a REST endpoint controller is in how the response is created.
//Rather than rely on a view (such as JSP) to render model data in HTML, an endpoint controller simply returns the data
//to be written directly to the body of the response.
//The @ResponseBody annotation tells Spring MVC not to render a model into a view, but rather to write the returned
//object into the response body. It does this by using one of Spring’s message converters. Because Jackson 2 is in the
//classpath, this means that MappingJackson2HttpMessageConverter will handle the conversion of User and Transaction to JSON
//if the request’s Accept header specifies that JSON should be returned.
//How do you know Jackson 2 is on the classpath? Either run ` mvn dependency:tree` or ./gradlew dependencies and you’ll
//get a detailed tree of dependencies which shows Jackson 2.x. You can also see that it comes from spring-boot-starter-web.


import com.memoer6.grocery.model.Product;
import com.memoer6.grocery.repository.ProductRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/v1/products")
@CrossOrigin   //enable CORS on all handler methods of this class
public class ProductController implements GrocerySvcAPI {

    @Autowired
    private ProductRepository productRepository;

    //List products from catalog
    @RequestMapping(method = RequestMethod.GET)
    @Override
    public List<Product> getProductsCatalog() {
        return productRepository.findAll();
    }

    //Add product to catalog
    @RequestMapping(method = RequestMethod.POST)
    @Override
    public Product addProductCatalog(@RequestBody Product product) {
        return productRepository.save(new Product(product.getName()));
    }

    //Update product from catalog
    @RequestMapping(value = "{productId}", method = RequestMethod.PUT)
    @Override
    public void updateProductCatalog(@PathVariable("productId") Long productId,
                                     @RequestBody Product product) {
        Optional<Product> optionalProduct = productRepository.findById(productId);
        if (optionalProduct.isPresent()) {
            productRepository.save(product);
        }
    }

    //Remove product from catalog
    @RequestMapping(value = "{productId}", method = RequestMethod.DELETE)
    @Override
    public void removeProductCatalog(@PathVariable("productId") Long productId) {
        productRepository.deleteById(productId);
    }

    //List products in shopping list  => product.inShoppingCart == true
    @RequestMapping(value = "shopping_cart", method = RequestMethod.GET)
    @Override
    public List<Product> getProductsShoppingList() {
        return productRepository.findByInShoppingCart(true);
    }

}
