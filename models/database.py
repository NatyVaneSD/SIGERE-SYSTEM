import sqlite3

def conectar_bd():
    return sqlite3.connect("banco.db")
def criar_tabelas():
    conexao = conectar_bd()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requisicao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_documento ENUM("FLAG","IPL", "BOP", "OF", "TCO", "MEMO") not null,
            numero_caso VARCHAR(30) not null,
            data_requisicao DATE not null,
            data_recebimento DATE not null,
            objetivo_pericia VARCHAR(50) not null,
            nivel_prioridade ENUM("P1", "P2", "P3", "P4") not null,
            pae_requisicao VARCHAR(50) not null,
            status_requisicao ENUM("ESPERA", "ANDAMENTO", "ENTREGUE", "TRANSFERIDO", "DEVOLVIDO", "CANCELADO") NOT NULL DEFAULT "EM ESPERA",
    )    
        CREATE TABLE IF NOT EXISTS autoridade_solicitante (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_solicitante VARCHAR (50) not null,

    )
        CREATE TABLE IF NOT EXISTS unidade_solicitante (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_unidade_solicitante VARCHAR (60) not null,

    )
        CREATE TABLE IF NOT EXISTS tipo_exame (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_exame VARCHAR(50) not null,

    )  
        CREATE TABLE IF NOT EXISTS protocolo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_protocolo VARCHAR(50) not null,
                data_entrega_perito DATE not null,
                perito ENUM ("MARCELO", "VERÔNICA", "NATANAEL", "LUIZ FERNANDO", "SAMIRA") not null,
    

    )  
        CREATE TABLE IF NOT EXISTS equipamento (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quantidade_equipamento INT not null,
    
    ) 
        CREATE TABLE IF NOT EXISTS tipo_equipamento (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_equipamento ENUM ("SMARTPHONE", "NOTEBOOK", "PENDRIVE", "CPU", "HD", "CARTÃO SSD") not null,
                outros_equipamentos VARCHAR (50)
    
    ) 
        CREATE TABLE IF NOT EXISTS armazenamento (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                deposito ENUM ("DEPÓSITO 1", "DEPÓSITO 2", "DEPÓSITO 3") not null,
                prateleira VARCHAR (20) not null,
                 
    ) 
        CREATE TABLE IF NOT EXISTS usuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login VARCHAR (225) not null, 
                senha VARCHAR (225) not null,
                nome_usuario VARCHAR (225) not null,
                tipo_usuario ENUM ("COMUM", "ADMINISTRATIVO", "GERENTE") not null,
                email_usuario VARCHAR (225) not null,            
    ) 
        CREATE TABLE IF NOT EXISTS laudo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_laudo VARCHAR (50) not null, 
                data_entrega_expedição DATE not null,
                data_entrega_custodia DATE not null,
                anexo_digital ENUM ("SIM", "NÃO") not null,
                perito ENUM ("MARCELO", "VERÔNICA", "NATANAEL", "LUIZ FERNANDO", "SAMIRA") not null,            
    ) 
        CREATE TABLE IF NOT EXISTS auditoria (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tabela_afetada VARCHAR (50) not null, 
                id_registro INT not null,
                id_usuario INT not null, 
                acao VARCHAR (50) not null,
                dados_antigos JSON not null,
                data_hora DATETIME not null, 
    ) 
           
    """)
    

    conexao.commit()
    conexao.close()

# Executar 
criar_tabelas()
print("Banco de dados criado com sucesso!")