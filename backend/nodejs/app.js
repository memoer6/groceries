
const express = require('express')
// Node.js body parsing middleware.This middleware parse incoming request bodies in a middleware before your 
// handlers. A new body object containing the parsed data is populated on the request object after the 
// middleware (i.e. req.body).
const bodyParser = require('body-parser')  
const routes = require('./routes')

const app = express()
const port = 8081  

// An Express application is essentially a series of middleware function calls.
// Middleware functions are functions that have access to the request object (req), the response object
// (res), and the next middleware function in the application’s request-response cycle. The next
// middleware function is commonly denoted by a variable named next.
// If the current middleware function does not end the request-response cycle, it must call next() to pass
// control to the next middleware function. Otherwise, the request will be left hanging.
// Bind application-level middleware to an instance of the app object by using the app.use()


// Returns middleware that only parses json and only looks at requests where the Content-Type header matches 
// the type option. This parser accepts any Unicode encoding of the body and supports automatic inflation
// of gzip and deflate encodings.
app.use(bodyParser.json());

// This example shows a middleware function with no mount path. The function is executed every time the app 
// receives a request.
app.use(function (req, res, next) {
  console.log('Time:', Date.now())
  next()
})

routes(app);
app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`)
})

app.use((error, req, res, next)=> {
  res.status(400).send(error)
})

