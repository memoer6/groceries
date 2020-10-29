package com.memoer6.grocery.repository;

import com.memoer6.grocery.model.Product;
import org.springframework.data.repository.CrudRepository;

import java.util.List;

//Boot is leveraging Spring Data for its Object Relational Mapping, and given that, we can leverage its conventions
// and mechanisms for working with databases. A convenient abstraction that Spring Data provides is the concept
// of a "repository", which is essentially a data access object (DAO) that is automatically wired together on our behalf.

// CrudRepository Spring Data JPA repositories are interfaces that you can define to access data. JPA queries are
// created automatically from your method names.
// For more complex queries you can annotate your method using Spring Data’s Query annotation.
//By default, JPA databases will be automatically created only if you use an embedded database (H2, HSQL or Derby)

// By extending CrudRepository, ItemRepository inherits several methods for working with Customer persistence,
// including methods for saving, deleting, and finding Item entities.
// Spring Data JPA also lets you define other query methods by declaring their method signature.


public interface ProductRepository extends CrudRepository<Product, Long> {

    // The native findAll method in JPA returns an Iterable object. This override method returns instead a List
    // so it can be returned to the client by the controller
    @Override
    List<Product> findAll();

    List<Product> findByInShoppingCart(boolean inShoppingCart);
}

//Spring Data can create implementations for you of @Repository interfaces of various flavors. Spring Boot will
//handle all of that for you as long as those @Repositories are included in the same package (or a sub-package)
//of your @EnableAutoConfiguration class.

//Spring Boot tries to guess the location of your @Repository definitions, based on the @EnableAutoConfiguration it finds.