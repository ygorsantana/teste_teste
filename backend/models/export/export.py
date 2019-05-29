from flask_restful import Resource, MethodView
from db import executeSql
from flask import jsonify
import models.productsCorello.export as CorelloExport
import models.productsLupo.export as LupoExport

class Export(MethodView):
    def post(self, store_id):
        response_object = {'status': 'success'}
        # Get ftp url
        row = executeSql('SELECT * FROM store WHERE id = {}'.format(store_id))[0]
        
        if 'corello' in str(row['ftp_url']).lower():
            CorelloExport.post(store_id)
        
        if 'lupo'in str(row['ftp_url']).lower():
            LupoExport.post(store_id)
        
        response_object['message'] = 'E-mail enviado com sucesso'

        return jsonify(response_object)
        
