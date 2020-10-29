const express = require('express'),
  app = express(),
  port = 8081


const product1 = {
  id: 1,
  name: 'bread',
  inCart: false
}

const product2 = {
  id: 2,
  name: 'butter',
  inCart: true
}

const products = [
  product1, product2
]

// An Express application is essentially a series of middleware function calls.
// Middleware functions are functions that have access to the request object (req), the response object
// (res), and the next middleware function in the application’s request-response cycle. The next
// middleware function is commonly denoted by a variable named next.
// If the current middleware function does not end the request-response cycle, it must call next() to pass
// control to the next middleware function. Otherwise, the request will be left hanging.

// Bind application-level middleware to an instance of the app object by using the app.use() 
// and app.METHOD() functions, where METHOD is the HTTP method of the request that the middleware 
// function handles (such as GET, PUT, or POST) in lowercase

// This example shows a middleware function with no mount path. The function is executed every time the app 
// receives a request.
app.use(function (req, res, next) {
  console.log('Time:', Date.now())
  next()
})


// Return the list of product in the catalog
app.get('/v1/products', (req, res) => {
  res.send(products)
})

// Add a new product to the catalog
app.post('/v1/products', (req, res) => {
})

// Update an existing product in the catalog
app.put('/v1/products/:productId', (req, res) => {
  res.send(req.params)
})

// Delete a product from the catalog
app.delete('/v1/products/:productId', (req, res) => {
  res.send(req.params)
})

// Returns the list of products to buy
app.get('/v1/products/shopping', (req, res) => {
  res.send(products)
})

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})

