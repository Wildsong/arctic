import os
import logging
from flask import Flask, render_template
import config

def handle_page_not_found(error):
    return render_template('404.html'), 404

def handle_bad_request(error):
    return 'bad request', 400
    

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
level = logging.WARN
if os.environ.get('FLASK_ENV') != 'production':
    level = logging.DEBUG
logging.getLogger().setLevel(level)
log = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(config.Config())
#print(app.config)
#for item in app.config:
#    print(item)

#assets_env.init_app(app)

# Add routes and custom error pages
    
# Load blueprints
from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

# Error handlers
app.register_error_handler(400, handle_bad_request)
app.register_error_handler(404, handle_page_not_found)

# That's all!

