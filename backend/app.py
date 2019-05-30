
# Imports from pip
from flask_cors import CORS
from flask_restful import Api, Resource
from flask import Flask

# Imports from files
from .models.flexy.flexy import Flexy

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
api = Api(app)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

def register_api(view, endpoint, url):
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, view_func=view_func, methods=['GET', 'POST'])


register_api(Flexy, 'flexy_api', '/flexyreceive/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
