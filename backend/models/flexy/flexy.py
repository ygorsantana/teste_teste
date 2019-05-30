from flask_restful import Resource, MethodView
from flask import request, jsonify, json
import json

class Flexy(MethodView):
    def get(self):
        response = request.get_json()
        
        if response:
            with open('{}.json'.format(response['customer']['tradeName']), 'w+') as f:
                f.write(json.dumps(response, indent=4, sort_keys=True))

        return jsonify({'Hello': 'World'})
            
    def post(self):
        response = request.get_json()
        
        if response:
            with open('{}.json'.format(response['customer']['tradeName']), 'w+') as f:
                f.write(json.dumps(response, indent=4, sort_keys=True))
        return jsonify({'Hello': 'World'})


    def delete(self, store_id):
        request.get_json()
        pass

    def put(self, store_id, product_id):
        request.get_json()
        pass