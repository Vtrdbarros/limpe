import pandas as pd
import json
import re
import sqlite3
from sqlite3 import Error
import time
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Função para carregar as regras de mapeamento e validação
def load_rules(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

# Função para mapear as colunas do DataFrame
def map_columns(df, column_mapping):
    column_map = {col: new_col for new_col, cols in column_mapping.items() for col in cols}
    df.rename(columns=column_map, inplace=True)
    return df

# Função para validar NCM
def validate_ncm(ncm):
    if isinstance(ncm, str) and len(ncm) in [7, 8]:
        return ncm.zfill(8)
    return None

# Função para validar descrição
def validate_description(description, patterns):
    if isinstance(description, str):
        for pattern in patterns:
            if re.search(pattern, description):
                return description
    return None

# Função para validar códigos
def validate_code(value, allowed_values):
    if value in allowed_values:
        return value
    return None

# Função genérica para validar padrões
def validate_generic(value, patterns):
    if isinstance(value, str):
        for pattern in patterns:
            if re.search(pattern, value):
                return value
    return None

# Função para aplicar validações no DataFrame
def apply_validations(df, validation_rules):
    for col, rules in validation_rules.items():
        if col in df.columns:
            if rules['type'] == 'string':
                if 'length' in rules:
                    df[col] = df[col].astype(str).apply(lambda x: x.zfill(rules['length'][0]) if len(x) in rules['length'] else None)
                if 'patterns' in rules:
                    df[col] = df[col].apply(lambda x: validate_generic(x, rules['patterns']))
                if 'allowed_values' in rules:
                    df[col] = df[col].apply(lambda x: validate_code(x, rules['allowed_values']))
    return df

# Função para criar a conexão com o banco de dados
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('limpe.db')  # Nome do arquivo do banco de dados
        print("Conexão estabelecida com SQLite.")
    except Error as e:
        print(f"Erro ao conectar ao SQLite: {e}")
    return conn

def select_csv_file():
    Tk().withdraw() # Oculta a janela principal do Tkinter
    filename = askopenfilename(filetypes=[("CSV files", "*.csv")])
    return filename

# Função para inserir dados no banco de dados
def insert_data(conn, df):
    try:
        start_time = time.time()  # Inicia um timer para medir o tempo de execução
        df.to_sql('Produtos', conn, if_exists='append', index=False)
        elapsed_time = time.time() - start_time  # Calcula o tempo de execução
        print(f"Dados inseridos com sucesso em {elapsed_time:.2f} segundos.")
    except Error as e:
        print(f"Erro ao inserir dados: {e}")

# Função principal para carregar, mapear, validar e inserir dados
def main():
    # Carregar regras de mapeamento e validação
    rules = load_rules('rules/mapping_validation.json')
    
    # Selecionar arquivo CSV pelo explorador de arquivos
    csv_file = select_csv_file()
    if not csv_file:
        print("Nenhum arquivo selecionado.")
        return

    # Carregar dados do CSV com codificação UTF-8
    data = pd.read_csv(csv_file, encoding='utf-8', on_bad_lines='skip')
    
    # Mapear colunas
    data = map_columns(data, rules['column_mapping'])
    
    # Aplicar validações
    data = apply_validations(data, rules['validation_rules'])
    
    # Criar conexão com o banco de dados
    conn = create_connection()
    
    # Inserir dados no banco de dados
    if conn is not None:
        insert_data(conn, data)
        conn.close()
    else:
        print("Erro! Não foi possível criar a conexão com o banco de dados.")

if __name__ == '__main__':
    main()
