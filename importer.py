import pandas as pd
import database

def process_file(file_path):
    # Lógica para importar diferentes tipos de arquivo e normalizar os dados
    conn = database.create_connection()
    data = pd.read_csv(file_path)  # Exemplo para CSV
    # Outras lógicas para XLS, XLSX, etc.
    # ...
    # Inserir dados no banco de dados
    with conn:
        data.to_sql('produtos', conn, if_exists='append', index=False)
