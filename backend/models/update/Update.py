import csv, os, psycopg2

from flask_restful import Resource, MethodView
from db import deleteInStore, executeSql, insertIntoStore
from flask import json, request, jsonify
from psycopg2.extras import RealDictCursor
from models.ftp_downloader.download import download_file
from models.productsCorello.query import createTable
from models.productsCorello.update import main as CorelloUpdate

class Update(MethodView):
    def post(self, store_id):
        response_object = {'status': 'success'}
        
        # Get ftp url
        row = executeSql('SELECT * FROM store WHERE id = {}'.format(store_id))[0]

        # Download and write on database
        download_file(row['ftp_url'])

        if 'corello' in str(row['ftp_url']).lower():
            CorelloUpdate(store_id)
        
        if 'lupo'in str(row['ftp_url']).lower():
            raise NotImplementedError

        response_object['message'] = 'Loja atualizada!'
        return response_object