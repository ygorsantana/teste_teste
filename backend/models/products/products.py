from flask_restful import Resource, MethodView
from flask import json, request, jsonify
from db import deleteInStore, executeSql, insertIntoStore
import models.productsCorello.products as Corello
import models.productsLupo.products as Lupo


class Products(MethodView):
    def get(self, store_id, product_id):
        # Get ftp url
        row = executeSql('SELECT * FROM store WHERE id = {}'.format(store_id))[0]

        if 'corello' in str(row['ftp_url']).lower():
            products = Corello.get(store_id, product_id)
        
        if 'lupo'in str(row['ftp_url']).lower():
            products = Lupo.get(store_id, product_id)
        
        return jsonify({
                            'products': products
                        })
            
    def post(self):
        pass


    def delete(self, store_id):
        pass

    def put(self, store_id, product_id):
        response_object = {'status': 'success'}
        
        row = executeSql('SELECT * FROM store WHERE id = {}'.format(store_id))[0]

        # Get response
        post_data = request.get_json()
        
        if 'corello' in str(row['ftp_url']).lower():
            Corello.put(store_id, product_id, post_data)
        
        if 'lupo'in str(row['ftp_url']).lower():
            Lupo.put(store_id, product_id, post_data)

        response_object['message'] = 'Loja atualizada!'
            
        return jsonify(response_object)