
const db = require('../db');

routes = function (app) {

  // app.METHOD() functions, where METHOD is the HTTP method of the request that the middleware 
  // function handles (such as GET, PUT, or POST) in lowercase

  // Get products 
  app.get('/v1/products', async (req, res, next) => {
    const { shop } = req.query
    const buy = (shop === 'true') ? true : false 
    // Express doesn't handle errors natively when invoking async function in routes 
    // These errors can be handled by try catch block 
    try {
      let { rows } = await db.query('SELECT * FROM products', null)
      // if query param "shop" is true, then filter the products to buy
      if (buy) rows = rows.filter(product => product.shopping_cart === true)
      // Return response
      res.status(200).send(rows)
    } catch (error) {      
      // For errors returned from asynchronous functions invoked by route handlers and middleware, you
      // must pass them to the next() function, where Express will catch and process them
      next(error)
    }    
  })

  // Create product  
  app.post('/v1/products', async (req, res, next) => {
    const { name } = req.body    
    // Check that 'name' property is sent in the request body 
    if (name === undefined) return res.status(400).send('Product name is required')
    try {   
      // Create product into database
      await db.query('INSERT INTO products (name, shopping_cart) VALUES ($1, $2)', [name, false])
      // Return product object to client
      const { rows } = await db.query('SELECT * FROM products WHERE name = $1', [name])
      res.status(201).send(rows[0])       
    } catch (error) {
      // Catched error when product is already registered (unique_violation)
      if (error.code === "23505") return res.status(400).send(`Product "${name}" is already registered`)
      next(error)
    }    
  })
  
   // Delete product  
   app.delete('/v1/products/:name', async (req, res, next) => {
    const { name } = req.params   
    try {
      // Delete product from database
      const { rowCount } = await db.query('DELETE FROM products WHERE name = $1', [name])
      // Product not found
      if ( rowCount === 0 ) return res.status(404).send(`Product "${name}" not found`)
      // Return response
      res.status(200).send(`Product "${name}" was deleted successfully`)
    } catch (error) {
      next(error)
    }    
  })



  // Update product 
  app.put('/v1/products/:name', async (req, res, next) => {
    const { name } = req.params
    // Check if json object is included in request body
    if (Object.keys(req.body).length === 0) return res.status(400).send('No product fields are detected')
    mutableProperties = ['shopping_cart']
    
    // Build SQL statement to update product
    // columnNames represents the set of column to set with $n placeholders for the SQL update statement
    let columnNames = ''
    // columnValues represents the list of values of the placeholders for the SQL update statement
    let columnValues = []
    // Object.entries returns [ key: value ] per each property 
    let propertiesToUpdate =  Object.entries(req.body).filter(prop => mutableProperties.includes(prop[0]))
    const propertiesToReject =  Object.entries(req.body)
              .filter(prop => !mutableProperties.includes(prop[0]))
              .map(prop => prop[0])
    propertiesToUpdate
              .map((prop, index) => { 
                columnNames += `${prop[0]} = $${index+1},`
                columnValues.push(prop[1])
              }) 
    propertiesToUpdate = propertiesToUpdate.map(prop => prop[0])                      
    columnNames = columnNames.slice(0, -1) // Remove last comma
    columnValues.push(name) // Add name for SQL WHERE condition
    const namePos = columnValues.length    // Index position for name value    
    const sql = `UPDATE products SET ${columnNames} WHERE name = $${namePos}`

    try {
      const { rowCount } = await db.query(sql, columnValues)
      // Product not found
       if ( rowCount === 0 ) return res.status(404).send(`Product "${name}" not found`)
      // Return response
      const msg = `Product: "${name}"\nFields updated: ${propertiesToUpdate}\nFields not updated: ${propertiesToReject}`
      res.status(200).send(msg)
    } catch (error) {
      next(error)
    }
    
  })

 
}  

  // export our routes to be mounted by the parent application
  module.exports = routes