import sqlite3

database_path = "pdf_data.db"

def select_data_from_database(database_path):
    try:
        # Conectar ao banco de dados SQLite
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        # Executar a query SELECT para buscar todos os dados da tabela pdf_data
        cursor.execute("SELECT * FROM pdf_data")
        rows = cursor.fetchall()

        # Exibir os dados retornados
        if rows:
            print("\n=== Dados Retornados da Tabela pdf_data ===")
            for row in rows:
                print(row)
        else:
            print("Nenhum dado encontrado na tabela pdf_data.")

    except sqlite3.Error as e:
        print(f"Erro ao selecionar dados do SQLite: {e}")

    finally:
        conn.close()

# Chamar a função para selecionar e exibir os dados da tabela pdf_data
select_data_from_database(database_path)
