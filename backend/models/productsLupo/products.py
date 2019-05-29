from flask_restful import Resource, MethodView
from flask import json, request, jsonify
from db import deleteInStore, executeSql, insertIntoStore
import psycopg2


def update_product(store_id, product_id, post_data):
    conn = psycopg2.connect(host='40.76.5.75', database='teste_database', user='db_napp', password='maker1001')
    cur = conn.cursor()

    corredor_template = str(post_data.get('corredor_template'))
    sub_corredor_template = str(post_data.get('sub_corredor_template'))
    nome_do_produto_template = str(post_data.get('nome_do_produto_template'))
    descricao_do_produto_template = str(post_data.get('descricao_do_produto_template'))
    preco_do_produto_template = str(post_data.get('preco_do_produto_template'))
    
    sql = '''
    UPDATE lupo
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
    #print('teste1')
    data = executeSql("SELECT * FROM lupo WHERE id_store = {} ORDER BY descricao_sku;".format(store_id))
    #print('teste2')
    products = list()
    #print('teste3')
    for row in data:
        product = dict()
        product['id'] = row['id']
        product['descricao_produto_completa'] = row['descricao_sku']
        product['codigo_barra'] = row['codigo']
        product['produto'] = row['descricao']
        product['estoque_final'] = row['estoque']
        product['preco1'] = row['preco']
        product['grupo_produto'] = row['setor']
        product['subgrupo_produto'] = row['linha']
        product['corredor_template'] = row['corredor_template']
        product['sub_corredor_template'] = row['sub_corredor_template']
        product['nome_do_produto_template'] = row['nome_do_produto_template']
        product['descricao_do_produto_template'] = row['descricao_do_produto_template']
        product['preco_do_produto_template'] = row['preco_do_produto_template']
        product['filled_template'] = row['filled_template']
        product['descricao_produto'] = row['descricao_sku'].split(',')[0]
        product['descricao_cor_produto'] = row['descricao_sku'].split(',')[2]
        products.append(product)
    #print('teste4')
    return products


def put(store_id, product_id, post_data):
    response_object = {'status': 'success'}

    # Update values
    update_product(store_id, product_id, post_data)

    response_object['message'] = 'Loja atualizada!'
        
    return jsonify(response_object)