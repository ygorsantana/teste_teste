import csv, os, re, sys, unicodedata
from bs4 import BeautifulSoup

tamanhos = dict()
tamanhos['PP'] = '2'
tamanhos['P'] = '3'
tamanhos['PLUS'] = '3'
tamanhos['M'] = '4'
tamanhos['G'] = '5'
tamanhos['GG'] = '6'
tamanhos['U'] = '7'
tamanhos['XG'] = '8'
tamanhos['XXG'] = '8'
tamanhos['XXXG'] = '9'


def getNpm(colorCode, productCode):
    #print(colorCode)
    for value in reversed(colorCode.split(' ')):
        try:
            cor = int(value)
            cor = value
        except:
            continue
    
    try:
        tamanho = tamanhos[colorCode.split(',')[1].upper().strip()]
    except:
        tamanho = ''
    
    return productCode.replace('"', '') + tamanho + cor


def getProductsLupo():
    soup = BeautifulSoup(open('./Lupo.xml', 'r').read(), 'html.parser')
    rel = soup.find_all('entry')

    produtosLupo = dict()
    for value in rel:
        seminpm = str(value.find('sku')).split('[CDATA[')[1].split(']]')[0]
        string = seminpm[:8] + seminpm[10:11] + seminpm[12:]
        produtosLupo[string] = value
    
    return produtosLupo

productsLupo = getProductsLupo()


def process_file():
    file_name = 'temp.csv'

    # Open file
    with open('./{}'.format(file_name), 'r') as f:
        # Create csv to write on
        file_writer = csv.writer(open('temp_writer.csv', 'w+'), delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        # Proccess csv opened
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            # Verify if product is available on stock
            if str(row[10]) == "0,00":
                continue

            # Create line to write on csv
            line = list()
            for col in row:
                line.append(col.replace('"', '').strip(' '))
            
            # Write on csv
            file_writer.writerow(line)


def removerAcentosECaracteresEspeciais(palavra):
    return ''.join(c for c in unicodedata.normalize('NFD', palavra) if unicodedata.category(c) != 'Mn')


# Format string from xml
def get_string_formatted(string):
    string = str(string)
    string = string.split('[CDATA[')[1].split(']]')[0]
    return string


def process_description(string):
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


# Get product from xml
def get_external_options(npm_produto):
    global productsLupo
    try:
        # Find product
        product = str(productsLupo[npm_produto])
        
        soup = BeautifulSoup(product, 'html.parser')
        
        nome_do_produto = removerAcentosECaracteresEspeciais(get_string_formatted(soup.find('nome_do_produto'))).replace("'", "")
        if len(nome_do_produto) > 64:
            nome_do_produto = nome_do_produto[:64]
        descricao_do_produto = process_description(get_string_formatted(soup.find('descricao'))).replace("'", "")
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
        fwrite.writerow(['codigo'.capitalize(), 'descricao sku'.capitalize(), 'referencia'.capitalize(), 'preco'.capitalize(), 'setor'.capitalize(), 'linha'.capitalize(), 'marca'.capitalize(), 'classificacao'.capitalize(), 'fornecedor'.capitalize(), 'descricao'.capitalize(), 'estoque'.capitalize(), 'Corredor','Subcorredor','Nome do Produto','Descricao do Produto','Preco do Produto'])

        for i, row in enumerate(csv.reader(open(file_to_process, 'r'), delimiter=';')):
            # Ignore header
            if i == 0:
                continue
            
            npm_produto = getNpm(row[1], row[2])
            external_options = get_external_options(npm_produto)

            if not external_options:
                continue

            row.append(row[4].replace('"','').split('-')[1].strip().capitalize()) # Corredor
            row.append(row[5].replace('"','').split('-')[1].strip().capitalize()) # Subcorredor
            row.append(external_options[0]) # Nome do Produto
            row.append(external_options[1]) # Descricao do Produto
            row.append(row[3].replace('"','').strip().capitalize()) # Preco do Produto
            fwrite.writerow(row)


def main():
    # process file
    if True:
        print('Processing file on Lupo:')
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

def teste():
    print(len(productsLupo))
    with open('teste.txt', 'w+') as f:
        for i, row in enumerate(csv.reader(open('../../temp_writer.csv', 'r'), delimiter=';')):
            # Ignore header
            if i == 0:
                continue
            
            npm_produto = getNpm(row[1], row[2])
            external_options = get_external_options(npm_produto)
            try:
                f.write(npm_produto + '\n')
                print(productsLupo[npm_produto])
            except:
                continue
            
            if not external_options:
                continue

if __name__ == "__main__":
    teste()