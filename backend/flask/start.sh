#!/usr/bin/env bash

export APP_PATH=~/code/groceries/backend/flask

# set environment variables
export $(cat $APP_PATH/../../.env)

# Own custom environment variable setting the configuration to run myapp. Possible values: dev, test, prod
export APP_CONFIG_ENV='test'   

# Flask detects factory method "create_app" in myapp package
export FLASK_APP="$APP_PATH/myapp:create_app('$APP_CONFIG_ENV')"

# If you enable debug support the server will reload itself on code changes, and it will also provide you with
# a helpful debugger if things go wrong.
export FLASK_ENV=development

# Create the database or enable migrations if the database already exists
#flask db init
# Generates a migration scripts
#flask db migrate
# Apply the migration to the database
#flask db upgrade

# Set OS environment variable to select the configuration file to load based on the deployment environment
# export APP_CONFIG_FILE=$PWD/config/development.py

# Start the web application 
flask run --host=0.0.0.0 --port=8081
