import psycopg2

from flask_restful import Resource, MethodView
from flask import json, request, jsonify
from db import deleteInStore, executeSql, insertIntoStore

def update_product(store_id, product_id, post_data):
    conn = psycopg2.connect(host='40.76.5.75', database='teste_database', user='db_napp', password='maker1001')
    cur = conn.cursor()

    corredor_template = str(post_data.get('corredor_template'))
    sub_corredor_template = str(post_data.get('sub_corredor_template'))
    nome_do_produto_template = str(post_data.get('nome_do_produto_template'))
    descricao_do_produto_template = str(post_data.get('descricao_do_produto_template'))
    preco_do_produto_template = str(post_data.get('preco_do_produto_template'))
    
    sql = '''
    UPDATE corello
    SET corredor_template = '{}',
    sub_corredor_template = '{}',
    nome_do_produto_template = '{}',
    descricao_do_produto_template = '{}',
    preco_do_produto_template = '{}',
    filled_template = true
    WHERE id_store = {} and id = {}
    '''.format(corredor_template, sub_corredor_template, nome_do_produto_template, descricao_do_produto_template, preco_do_produto_template, store_id, product_id)
    
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

def get(store_id, product_id):
    data = executeSql("SELECT * FROM corello WHERE id_store = {} ORDER BY descricao_produto;".format(store_id))
    products = json.loads(json.dumps(data))
    return products
        

def put(store_id, product_id, post_data):
    response_object = {'status': 'success'}

    # Update values
    update_product(store_id, product_id, post_data)

    response_object['message'] = 'Loja atualizada!'
        
    return jsonify(response_object)
    