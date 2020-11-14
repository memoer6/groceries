
// PostgreSQL
// node-postgres is a collection of node.js modules for interfacing with your PostgreSQL database
// If you're working on a web application or other software which makes frequent queries you'll
// want to use a connection pool.

const { Pool } = require('pg')


const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'grocery-db',
  password: 'my_secret',
  port: 5432,
})


module.exports = {  
  query: (text, params) => pool.query(text, params)
}


