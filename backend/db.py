import psycopg2
from psycopg2.extras import RealDictCursor


def executeSql(sql):
    conn = psycopg2.connect(host='40.76.5.75', database='teste_database', user='db_napp', password='maker1001')
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(sql)
    query_executed = cur.fetchall()
    cur.close()
    conn.close()
    return query_executed


def insertIntoStore(logradouro, nome, telefone, endereco, horarios, ftp_url):
    conn = psycopg2.connect(host='40.76.5.75', database='teste_database', user='db_napp', password='maker1001')
    sql = '''INSERT INTO store(logradouro, nome, telefone, endereco, horarios, ftp_url)
                        VALUES(        %s,   %s,       %s,       %s,       %s,      %s) '''
    
    
    cur = conn.cursor()
    cur.execute(sql, (logradouro, nome, telefone, endereco, horarios, ftp_url,))

    conn.commit()
    cur.close()
    conn.close()


def updateOnStore(store_id, logradouro, nome, telefone, endereco, horarios, ftp_url):
    conn = psycopg2.connect(host='40.76.5.75', database='teste_database', user='db_napp', password='maker1001')
    sql = ''' UPDATE store
    SET logradouro = '{}',
    nome = '{}',
    telefone = '{}',
    endereco = '{}',
    horarios = '{}',
    ftp_url = '{}'
    WHERE id = {}'''.format(logradouro, nome, telefone, endereco, horarios, ftp_url, store_id)
    cur = conn.cursor()
    cur.execute(sql, (logradouro, nome, telefone, endereco, horarios, ftp_url,))

    conn.commit()
    cur.close()
    conn.close()


def deleteInStore(store_id):
    conn = psycopg2.connect(host='40.76.5.75', database='teste_database', user='db_napp', password='maker1001')
    cur = conn.cursor()
    
    cur.execute("DELETE FROM corello WHERE id_store = {}; DELETE FROM store WHERE id = {};".format(int(store_id), int(store_id)))
    conn.commit()
    cur.close()
    conn.close()
