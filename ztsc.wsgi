import sys
import os

# Add your project directory to the sys.path
project_dir = '/var/www/apps/ztsc'
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

# Set the environment variable for the Flask application
os.environ['FLASK_APP'] = 'ztsc'

# Import the Flask app object
from ztsc import app as application
