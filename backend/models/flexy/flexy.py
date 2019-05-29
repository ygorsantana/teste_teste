from flask_restful import Resource, MethodView
from flask import json, request, jsonify


class Flexy(MethodView):
    def get(self):
        return jsonify({'Hello': 'World'})
            
    def post(self):
        pass


    def delete(self, store_id):
        pass

    def put(self, store_id, product_id):
        pass