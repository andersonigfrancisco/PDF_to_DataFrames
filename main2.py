import camelot
import pandas as pd

file_path = "TEST2.pdf"

def process_pdf(file_path):
    try:
        # Extrair tabelas do PDF usando Camelot
        tables = camelot.read_pdf(file_path, pages='all', flavor='stream', strip_text='\n')

        if not tables:
            print("Nenhuma tabela encontrada no arquivo PDF.")
        else:
            # Inicializar uma lista para armazenar os DataFrames
            dfs = []

            for i, table in enumerate(tables):
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

                # Ajustar o DataFrame final para o formato desejado
                final_df.columns = final_df.iloc[0]  # Definir a primeira linha como cabeçalho
                final_df = final_df.drop([0]).reset_index(drop=True)  # Remover a primeira linha

                # Imprimir o DataFrame final com formatação de tabela
                print("\n=== DataFrame Final Concatenado ===")
                print(final_df.to_string(index=False))

            else:
                print("Nenhum DataFrame válido encontrado.")

    except FileNotFoundError:
        print(f"Arquivo PDF não encontrado: {file_path}")
    except Exception as e:
        print(f"Erro ao processar o PDF: {e}")

# Chamar a função para processar o PDF
process_pdf(file_path)