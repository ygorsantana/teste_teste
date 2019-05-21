
# Imports from pip
from flask_cors import CORS
from flask_restful import Api, Resource
from flask import Flask

# Imports from files
from models.productsCorello.export import Export
from models.productsCorello.products import Products
from models.productsCorello.update import Update
from models.store.store import Store

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
api = Api(app)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

def register_api(view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None},
                    view_func=view_func, methods=['GET',])
    app.add_url_rule(url, view_func=view_func, methods=['POST',])
    app.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
                    methods=['GET', 'PUT', 'DELETE'])


register_api(Store, 'store_api', '/stores/', pk='store_id')
register_api(Products, 'product_api', '/stores/<store_id>/products/', pk='product_id')
api.add_resource(Update, '/stores/<store_id>/update')
api.add_resource(Export, '/stores/<store_id>/export')

if __name__ == '__main__':
    app.run()
