package com.memoer6.grocery.model;

import com.sun.istack.NotNull;

import javax.persistence.*;


//Entities in JPA are nothing but POJOs representing data that can be persisted to the database. An entity represents
// a table stored in a database. Every instance of an entity represents a row in the table
// This application uses the Jackson JSON library to automatically marshal instances of type Item into JSON.
// Jackson is included by default by the web starter.
// If @Table annotation is not included, then it is assumed that this entity is mapped to a table named Item

@Entity
@Table(name = "Products")
public class Product {

    // Each JPA entity must have a primary key which uniquely identifies it. The @Id annotation defines the
    // primary key. We can generate the identifiers in different ways which are specified by the @GeneratedValue annotation.
    // If we specify GenerationType.AUTO, the JPA provider will use any strategy it wants to generate the identifiers.
    @Id
    @GeneratedValue(strategy= GenerationType.AUTO)
    private Long id;

    @NotNull
    private String name;

    private Boolean inShoppingCart = Boolean.FALSE;

    // No-args constructor required by JPA spec. This one is protected since it shouldn't be used directly
    protected Product() {}

    // The other constructor is the one you use to create instances of Item to be saved to the database
    public Product(String name) {
        this.name = name;
    }

    public Long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Boolean getInShoppingCart() {
        return inShoppingCart;
    }

    public void setInShoppingCart(Boolean inShoppingCart) {
        this.inShoppingCart = inShoppingCart;
    }

    // The convenient toString() method print outs the customer’s properties
    @Override
    public String toString() {
        return "Item [id=" + id + ", name=" + name + ", inShoppingCart="
                + inShoppingCart + "]";
    }
}
