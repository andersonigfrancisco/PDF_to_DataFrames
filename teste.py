import camelot
import pandas as pd

file_path = "Teste.pdf"

try:
    # Lê todas as tabelas do PDF usando o flavor 'stream'
    tables = camelot.read_pdf(file_path, pages='all', flavor='stream')

    # Verifica se alguma tabela foi encontrada
    if not tables or len(tables) == 0:
        print("Nenhuma tabela encontrada no arquivo PDF.")
    else:
        # Exibe a estrutura das tabelas encontradas
        for i, table in enumerate(tables):
            print(f"Tabela {i + 1}:")
            print(table.df)
            print("\n")

except Exception as e:
    print(f"Erro ao processar o PDF: {e}")
