import sqlite3
from sqlite3 import Error
import time

def create_connection():
    """ Cria uma conexão com o banco de dados SQLite especificado """
    conn = None
    try:
        conn = sqlite3.connect('limpe.db')  # Nome do arquivo do banco de dados
        print("Conexão estabelecida com SQLite.")
    except Error as e:
        print(f"Erro ao conectar ao SQLite: {e}")
    return conn

def create_table(conn, create_table_sql):
    """ Cria uma tabela a partir do create_table_sql passado """
    try:
        start_time = time.time()  # Inicia um timer para medir o tempo de execução
        c = conn.cursor()
        c.execute(create_table_sql)
        elapsed_time = time.time() - start_time  # Calcula o tempo de execução
        print(f"Tabela criada com sucesso em {elapsed_time:.2f} segundos.")
    except Error as e:
        print(f"Erro ao criar tabela: {e}")

def main():
    sql_create_produtos_table = """ CREATE TABLE IF NOT EXISTS Produtos (
                                        ProdutoID integer PRIMARY KEY,
                                        Descricao text NOT NULL,
                                        CodigoNCM text,
                                        CodigoEAN text,
                                        DataAtualizacao text
                                    ); """

    sql_create_tributacao_table = """ CREATE TABLE IF NOT EXISTS TributacaoICMS (
                                        TributacaoID integer PRIMARY KEY,
                                        ProdutoID integer NOT NULL,
                                        CSTICMS text,
                                        CEST text,
                                        CSTPISCOFINS text,
                                        NatRecPISCOFINS text,
                                        RegimeTributario text,
                                        DataAtualizacao text,
                                        FOREIGN KEY (ProdutoID) REFERENCES Produtos (ProdutoID)
                                    ); """

    # Cria uma conexão com o banco de dados
    conn = create_connection()

    # Cria as tabelas
    if conn is not None:
        print("Iniciando a criação de tabelas...")
        create_table(conn, sql_create_produtos_table)
        create_table(conn, sql_create_tributacao_table)
        conn.close()
        print("Banco de dados configurado com sucesso.")
    else:
        print("Erro! Não foi possível criar a conexão com o banco de dados.")

if __name__ == '__main__':
    main()
