from bs4 import BeautifulSoup

def getNpm(string):
    string = string.split('[CDATA[')[1].split(']]')[0].split('_')
    string.pop()
    string = "_".join(string)
    return string


def getProductsCorello():
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(open('./Corello.xml', 'r').read(), 'html.parser')
    rel = soup.find_all('entry')

    produtosCorello = dict()
    for value in rel:
        string = getNpm(str(value.find('g:mpn'))[:-2])
        produtosCorello[string] = value
    
    return produtosCorello

productsCorello = getProductsCorello()

import csv, os, re, sys, unicodedata

def process_file():
    file_name = 'temp.csv'
    # Open file
    with open('./{}'.format(file_name), 'r') as f:
        # Create csv to write on
        file_writer = csv.writer(open('temp_writer.csv', 'w+'), delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        # process csv opened
        for row in csv.reader(f, delimiter=';'):
            # Verify if product is available on stock
            if str(row[5]) == '0':
                continue
            
            # Create line to write on csv
            line = list()
            for col in row:
                line.append(col.replace('"', '').strip(' '))
            
            # Write on csv
            file_writer.writerow(line)


def removerAcentosECaracteresEspeciais(palavra):
    return ''.join(c for c in unicodedata.normalize('NFD', palavra) if unicodedata.category(c) != 'Mn')


def process_description(string):
    string = string.replace('<h5>', '').replace('</h5>', '').replace('<strong>', '').replace('</strong>', '')

    newLine = list()
    for line in string.split('.'):
        if line:
            newLine.append(line.strip())
            
    string = "\n".join(newLine)
    newLine = list()
    for line in removerAcentosECaracteresEspeciais(string).split('\n'):
        if line:
            newLine.append(line.strip())
    string = ". ".join(newLine) 

    return string
    

# Format string from xml
def get_string_formatted(string):
    string = str(string)
    string = string.split('[CDATA[')[1].split(']]')[0]
    return string


# Get product from xml
def get_external_options(npm_produto):
    global productsCorello
    try:
        # Find product
        #print(npm_produto)
        product = str(productsCorello[npm_produto])
        
        soup = BeautifulSoup(product, 'html.parser')
        
        nome_do_produto = removerAcentosECaracteresEspeciais(get_string_formatted(soup.find('title'))).replace("'", "")
        if len(nome_do_produto) > 64:
            nome_do_produto = nome_do_produto[:64]
        descricao_do_produto = process_description(get_string_formatted(soup.find('g:description'))).replace("'", "")
        if len(descricao_do_produto) > 1000:
            descricao_do_produto = descricao_do_produto[:1000]

    except KeyboardInterrupt:
        sys.exit(0)
    
    except KeyError:
        return ''

    return [nome_do_produto, descricao_do_produto]


def process_file_2():
    file_to_process = 'temp_writer.csv'
    file_processed = 'temp_writer2.csv'

    with open(file_processed, 'w+') as csvfile:
        fwrite = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        fwrite.writerow(["CODIGO_BARRA".capitalize(),"DESC_COR_PRODUTO".capitalize(),"TAMANHO".capitalize(),"GRADE".capitalize(),"PRODUTO".capitalize(),"ESTOQUE".capitalize(),"RESERVA".capitalize(),"ESTOQUE_FINAL".capitalize(),"CODIGO_TAB_PRECO".capitalize(),"PRECO1".capitalize(),"TIPO_PRODUTO".capitalize(),"DESC_PRODUTO".capitalize(),"DESC_PROD_NF".capitalize(),"GRUPO_PRODUTO".capitalize(),"SUBGRUPO_PRODUTO".capitalize(),"LINHA".capitalize(),"MARCA".capitalize(),"UNIDADE".capitalize(),"PESO".capitalize(),"REFER_FABRICANTE".capitalize(),"FABRICANTE".capitalize(),"ESTILISTA".capitalize(),"SEXO_TIPO".capitalize(),"ULTIMA_SAIDA".capitalize(),"ULTIMA_ENTRADA".capitalize(),"FILIAL".capitalize(),"COR_PRODUTO".capitalize(),"COLECAO".capitalize(),"ORIGEM".capitalize(),"MATERIAL".capitalize(),"DATA_CADASTRAMENTO".capitalize(),"CONCAT_DESC_PRODUTO".capitalize(),'Corredor'.capitalize(),'Subcorredor'.capitalize(),'Nome do Produto'.capitalize(),'Descricao do Produto'.capitalize(),'Preco do Produto'])
        
        for row in csv.reader(open(file_to_process, 'r'), delimiter=';'):
            npm_produto = row[4] + '_' + row[26]

            # Search a letter on npm_produto
            if len(re.findall('[A-Za-z]+', npm_produto)):
                continue
            
            external_options = get_external_options(npm_produto)
            if not external_options:
                # Remove this commentary if wanna submit on database rows not found on XML
                #fwrite.writerow([row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],row[19],row[20],row[21],row[22],row[23],row[24],row[25],row[26],row[27],row[28],row[29],row[30],row[31], '', '', '', '', ''])
                continue


            # === Essentials ===
            corredor = row[13].capitalize()
            subcorredor = row[14].capitalize()
            nome_do_produto = external_options[0] #
            descricao_do_produto = external_options[1] #
            preco_do_produto = row[9] #
            # ==================

            fwrite.writerow([row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],row[19],row[20],row[21],row[22],row[23],row[24],row[25],row[26],row[27],row[28],row[29],row[30],row[31], corredor, subcorredor, nome_do_produto, descricao_do_produto, preco_do_produto])
    
    #os.rename(file_in, path_out)


def main():
    # process file
    if True:
        print('Processing file on Corello:')
        print('Making 1st process...')
        process_file()
        print('Finished.\nMaking 2nd process...')
        process_file_2()
        print('Finished.')
    
    print('Removing temp files...')
    try:
        os.remove('temp.csv')
        os.remove('temp_writer.csv')
    except:
        pass