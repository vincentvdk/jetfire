# import
from flask import send_file, Blueprint, Flask, send_from_directory
from app import app

# Frontend blueprint
frontend_blueprint = Blueprint(
    'frontend', __name__, template_folder='templates', static_folder='static'
)

# Path to the folder we're serving our static files from
#app.config['static'] = '/path/to/flask-ember/static'


#@app.route('/static/<path:filename>')
#def send_resource(filename):
#    return send_from_directory(app.config['static'], filename)


#@frontend_blueprint.route('/')
#def home():
#    return send_file('frontend/templates/ember_index.html')


@frontend_blueprint.route('/')
def home():
    return send_file('frontend/templates/backbone_index.html')
