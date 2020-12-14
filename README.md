
Web service to manage a grocery list

Backends:

springboot: This backend consists of a Spring boot server exposing a REST API to add and remove items to/from a shopping list.
The data is stored in an embedded (in memory) database (H2). This example needs the JPA and H2 dependencies.

nodejs: This backend consists of a Node.js server exposing a REST API to add and remove items to/from a shopping list.

flask: This backend consists of a Flask server exposing a REST API to add and remove items to/from a shopping list. The server is integrated with local sqlite3 database in development environment, and PostgreSQL database in test environment. It implements Flask SQLAlchemy library for both integrations


review: https://github.com/cookiecutter-flask


