from myapp import create_app
import os

# When setting up a production web server to point to your app, you will almost always configure it to point
# to wsgi.py, which in turn imports and starts our entire app

# Set OS environment variable to select the configuration file to load based on the deployment environment
os.environ["APP_CONFIG_FILE"] = os.path.join(os.getcwd(), 'config/production.py')

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081)