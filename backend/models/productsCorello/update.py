import csv, os, psycopg2

from flask_restful import Resource, MethodView
from db import deleteInStore, executeSql, insertIntoStore
from flask import json, request, jsonify
from psycopg2.extras import RealDictCursor
from models.ftp_downloader.download import download_file
from models.productsCorello.query import createTable
from models.productsCorello.process import main as CorelloMain

def main(store_id):
    CorelloMain()
    write_on_database(store_id)

    # Remove remaining files
    print('Removing last file...')
    os.remove('temp_writer2.csv')
    print('Removed !!!')
    print('Everything up-to-date')



def write_on_database(store_id):
    conn = psycopg2.connect(host='40.76.5.75', database='teste_database', user='db_napp', password='maker1001')
    cur = conn.cursor()
    cur.execute('''DELETE FROM corello WHERE id_store = {}'''.format(store_id))
    #cur.execute(createTable)
    conn.commit()
    sql = '''INSERT INTO corello(id_store, codigo_barra, descricao_cor_produto, tamanho, grade, produto, estoque, reserva, estoque_final, codigo_tab_preco, preco1, tipo_produto, descricao_produto, descricao_produto_nf, grupo_produto, subgrupo_produto, linha, marca, unidade, peso, referencia_fabricante, fabricante, estilista, sexo_tipo, ultima_saida, ultima_entrada, filial, cor_produto, colecao, origem, material, data_cadastramento, descricao_produto_completa, corredor_template, sub_corredor_template, nome_do_produto_template, descricao_do_produto_template, preco_do_produto_template, filled_template) VALUES '''

    valuesSql = list()
    # process csv opened
    for i, row in enumerate(csv.reader(open('./temp_writer2.csv', 'r'), delimiter=';')):
        if i == 0:
            continue

        valuesSql.append("({}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', false)".format(store_id, *row))
    
    cur.execute(sql + ", ".join(valuesSql))
    cur.close()
    conn.commit()
    conn.close()
    