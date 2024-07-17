from pathlib import Path
from flask import Flask, render_template
import pkgutil
import importlib
from dotenv import load_dotenv

def create_app():
    # Load environment variables from .env file
    load_dotenv()

    # Create a Path object
    template_path = Path('templates')

    # Get the absolute path
    abs_template_path = template_path.resolve()
    
    # Create the Flask app with the specified template folder
    app = Flask(__name__, template_folder=abs_template_path)
    app.config['EXPLAIN_TEMPLATE_LOADING'] = True
    
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

# Add the home page
@app.route('/')
def home():
    return render_template('home.html')

# if "__main__" then run as Debug Mode on local PC
if __name__ == '__main__':
    app.run(debug=True)
