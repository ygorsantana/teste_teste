DROP TABLE IF EXISTS corello, lupo, store;

CREATE TABLE IF NOT EXISTS store
(   
    id SERIAL PRIMARY KEY,
    logradouro VARCHAR(255),
    nome VARCHAR(255),
    telefone VARCHAR(30),
    endereco VARCHAR(255),
    horarios VARCHAR(30),
    ftp_url VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS corello
(   
    id SERIAL PRIMARY KEY,
    id_store INT REFERENCES store(id),
    codigo_barra VARCHAR(255),
    descricao_cor_produto VARCHAR(255),
    tamanho VARCHAR(255),
    grade VARCHAR(255),
    produto VARCHAR(255),
    estoque VARCHAR(255),
    reserva VARCHAR(255),
    estoque_final VARCHAR(255),
    codigo_tab_preco VARCHAR(255),
    preco1 VARCHAR(255),
    tipo_produto VARCHAR(255),
    descricao_produto VARCHAR(255),
    descricao_produto_nf VARCHAR(255),
    grupo_produto VARCHAR(255),
    subgrupo_produto VARCHAR(255),
    linha VARCHAR(255),
    marca VARCHAR(255),
    unidade VARCHAR(255),
    peso VARCHAR(255),
    referencia_fabricante VARCHAR(255),
    fabricante VARCHAR(255),
    estilista VARCHAR(255),
    sexo_tipo VARCHAR(255),
    ultima_saida VARCHAR(255),
    ultima_entrada VARCHAR(255),
    filial VARCHAR(255),
    cor_produto VARCHAR(255),
    colecao VARCHAR(255),
    origem VARCHAR(255),
    material VARCHAR(255),
    data_cadastramento VARCHAR(255),
    descricao_produto_completa VARCHAR(255),
    corredor_template VARCHAR(30),
    sub_corredor_template VARCHAR(30),
    nome_do_produto_template VARCHAR(64),
    descricao_do_produto_template VARCHAR(1000),
    preco_do_produto_template VARCHAR(30),
    filled_template BOOLEAN
);

CREATE TABLE IF NOT EXISTS lupo
(   
    id SERIAL PRIMARY KEY,
    id_store INT REFERENCES store(id),
    codigo VARCHAR(255),
    descricao_sku VARCHAR(255),
    referencia VARCHAR(255),
    preco VARCHAR(255),
    setor VARCHAR(255),
    linha VARCHAR(255),
    marca VARCHAR(255),
    classificacao VARCHAR(255),
    fornecedor VARCHAR(255),
    descricao VARCHAR(255),
    estoque VARCHAR(255),
    corredor_template VARCHAR(30),
    sub_corredor_template VARCHAR(30),
    nome_do_produto_template VARCHAR(64),
    descricao_do_produto_template VARCHAR(1000),
    preco_do_produto_template VARCHAR(30),
    filled_template BOOLEAN
);
