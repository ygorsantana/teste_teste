from flask_restful import Resource, MethodView
from flask import json, request, jsonify
from db import deleteInStore, executeSql, insertIntoStore, updateOnStore
from psycopg2.extras import RealDictCursor


def remove_store(store_id):
    for store in executeSql("SELECT * from store"):
        if store['id'] == store_id:
            deleteInStore(store_id)
            return True

    return False

class Store(MethodView):
    def get(self, store_id):
        stores = json.loads(json.dumps(executeSql("SELECT * FROM store")))
        return jsonify({
                            'stores': stores
                        })
            
    def post(self):
        response_object = {'status': 'success'}

        # Get response
        post_data = request.get_json()
        
        # Fill fields
        logradouro = post_data.get('logradouro')
        nome = post_data.get('nome')
        telefone = post_data.get('telefone')
        endereco = post_data.get('endereco')
        horarios = post_data.get('horarios')
        ftp_url = post_data.get('ftp_url')

        # Call insert
        insertIntoStore(logradouro, nome, telefone, endereco, horarios, ftp_url)
        response_object['message'] = 'Loja adicionada!'
            
        return jsonify(response_object)


    def delete(self, store_id):
        response_object = {'status': 'success'}
        remove_store(store_id)
        response_object['message'] = 'Loja removida!'

        return jsonify(response_object)

    def put(self, store_id):
        response_object = {'status': 'success'}
            
        # Get response
        post_data = request.get_json()
        
        # Fill fields
        logradouro = post_data.get('logradouro')
        nome = post_data.get('nome')
        telefone = post_data.get('telefone')
        endereco = post_data.get('endereco')
        horarios = post_data.get('horarios')
        ftp_url = post_data.get('ftp_url')

        # Call insert
        updateOnStore(store_id, logradouro, nome, telefone, endereco, horarios, ftp_url)

        response_object['message'] = 'Loja atualizada!'
            
        return jsonify(response_object)
    