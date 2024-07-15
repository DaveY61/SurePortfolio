from flask import Flask
import pkgutil
import importlib
from dotenv import load_dotenv

def create_app():
    # Load environment variables from .env file
    load_dotenv()
    
    # Define the Flask app
    app = Flask(__name__)
    
    # Dynamically discover and register blueprints
    register_blueprints(app, 'services')

    return app

def register_blueprints(app, package_name):
    package = importlib.import_module(package_name)
    for _, module_name, is_pkg in pkgutil.iter_modules(package.__path__):
        if is_pkg:
            continue
        module = importlib.import_module(f"{package_name}.{module_name}")
        if hasattr(module, 'blueprint'):
            app.register_blueprint(getattr(module, 'blueprint'))

# Create the app to serve the site
app = create_app()

# Add the default page
@app.route('/')
def hello_world():
    return 'This is SurePortfolio!'

# if "__main__" then run as Debug Mode on local PC
if __name__ == '__main__':
    app.run(debug=True)
