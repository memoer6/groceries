#!/usr/bin/env bash

export FLASK_APP=myapp

# If you enable debug support the server will reload itself on code changes, and it will also provide you with
# a helpful debugger if things go wrong.
export FLASK_ENV=development

# Set OS environment variable to select the configuration file to load based on the deployment environment
export APP_CONFIG_FILE=$PWD/config/development.py

# Reset the sqlite3 database
flask init-db

# Start the web application for development
flask run --host=0.0.0.0 --port=8081
