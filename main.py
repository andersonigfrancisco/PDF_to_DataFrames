import camelot
import pandas as pd
import sqlite3

file_path = "TEST2.pdf"
database_path = "pdf_data.db"

def create_database_table(final_df):
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    try:
        # Verificar se o DataFrame final está vazio
        if final_df.empty:
            print("O DataFrame final está vazio. Nenhuma tabela será criada no banco de dados.")
            return

        # Limpar a tabela existente (opcional)
        cursor.execute("DROP TABLE IF EXISTS pdf_data")
        conn.commit()

        # Montar a query para criar a tabela com base nas colunas do DataFrame final
        columns = final_df.columns.tolist()
        column_types = ['TEXT'] * len(columns)  # Definir todas as colunas como TEXT por padrão para SQLite

        query = f"CREATE TABLE IF NOT EXISTS pdf_data ({', '.join([f'{col} {ctype}' for col, ctype in zip(columns, column_types)])})"
        cursor.execute(query)

        conn.commit()
        print("Tabela criada no banco de dados SQLite.")

    except sqlite3.Error as e:
        print(f"Erro ao criar tabela no SQLite: {e}")

    finally:
        conn.close()

def process_pdf_and_store(file_path):
    try:
        # Extrair tabelas do PDF usando Camelot
        tables = camelot.read_pdf(file_path, pages='all', flavor='stream', strip_text='\n')

        if not tables:
            print("Nenhuma tabela encontrada no arquivo PDF.")
        else:
            # Inicializar uma lista para armazenar os DataFrames
            dfs = []

            for table in tables:
                # Obter o DataFrame da tabela atual
                df = table.df

                # Remover linhas completamente vazias
                df = df.dropna(how='all').reset_index(drop=True)

                # Preencher células vazias com strings vazias
                df = df.replace(r'^\s*$', '', regex=True)

                # Adicionar DataFrame ajustado à lista, se não estiver vazio
                if not df.empty:
                    dfs.append(df)

            if dfs:
                # Concatenar todos os DataFrames da lista final
                final_df = pd.concat(dfs, ignore_index=True)

                # Gerar nomes de coluna automáticos se estiverem vazios ou não especificados
                final_df.columns = [f"Column_{idx+1}" if not isinstance(col, str) or col.strip() == '' else col.strip() for idx, col in enumerate(final_df.columns)]

                # Imprimir o DataFrame final com formatação de tabela
                print("\n=== DataFrame Final Concatenado ===")
                print(final_df.to_string(index=False))

                # Criar a tabela no banco de dados SQLite baseado no DataFrame final
                create_database_table(final_df)

                # Verificar se as colunas do DataFrame final correspondem às da tabela no banco de dados SQLite
                conn = sqlite3.connect(database_path)
                db_columns = pd.read_sql("PRAGMA table_info('pdf_data')", conn)['name'].tolist()
                conn.close()

                if set(final_df.columns) != set(db_columns):
                    raise ValueError("As colunas do DataFrame final não correspondem às colunas da tabela no banco de dados SQLite.")

                # Inserir dados no banco de dados SQLite
                conn = sqlite3.connect(database_path)
                final_df.to_sql('pdf_data', conn, if_exists='append', index=False)
                conn.close()

                print("\nDados inseridos com sucesso no banco de dados SQLite.")

            else:
                print("Nenhum DataFrame válido encontrado.")

    except FileNotFoundError:
        print(f"Arquivo PDF não encontrado: {file_path}")
    except ValueError as ve:
        print(f"Erro ao processar o PDF: {ve}")
    except Exception as e:
        print(f"Erro inesperado ao processar o PDF: {e}")

# Chamar a função para processar o PDF e inserir os dados no SQLite
process_pdf_and_store(file_path)
