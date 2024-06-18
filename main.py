import camelot
import pandas as pd
from tabulate import tabulate
import itertools

file_path = "TEST2.pdf"

try:
    # Extrair tabelas do PDF usando Camelot
    tables = camelot.read_pdf(file_path, pages='all', flavor='stream', strip_text='\n')

    if not tables:
        print("Nenhuma tabela encontrada no arquivo PDF.")
    else:
        # Inicializar uma lista vazia para armazenar os DataFrames
        dfs = []

        for table in tables:
            # Obter o DataFrame da tabela atual
            df = table.df

            # Remover linhas completamente vazias e linhas com células vazias
            df = df.dropna(how='all').reset_index(drop=True)

            # Verificar se há células vazias na primeira coluna e ajustar se necessário
            if pd.isna(df.iloc[0, 0]):
                df.iloc[0, 0] = df.iloc[1, 0]

            # Adicionar o DataFrame ajustado à lista
            dfs.append(df)

        # Concatenar todos os DataFrames da lista final
        final_df = pd.concat(dfs, ignore_index=True)

        # Converter todas as colunas que podem ser convertidas para numérico
        for col in final_df.columns:
            try:
                final_df[col] = pd.to_numeric(final_df[col].str.replace(',', ''), errors='raise')
            except:
                continue

        # Preencher valores faltantes com um valor padrão (zero)
        final_df = final_df.fillna(0)

        # Definir um limite de caracteres por linha para evitar distorções
        max_chars_per_line = 100

        # Imprimir o DataFrame final com tabulate com paginação e ajuste automático de colunas
        headers = final_df.columns.tolist()
        rows = final_df.values.tolist()

        # Tamanho máximo de linhas por página
        max_rows_per_page = 20

        for page in itertools.zip_longest(*[iter(rows)]*max_rows_per_page):
            page = [item for item in page if item is not None]

            # Ajuste automático de largura das colunas
            colalign = ['left'] * len(headers)

            # Limitar caracteres por linha para evitar distorções
            page_formatted = []
            for row in page:
                row_formatted = []
                for col_idx, col_value in enumerate(row):
                    if isinstance(col_value, str) and len(col_value) > max_chars_per_line:
                        col_value = col_value[:max_chars_per_line] + '...'
                    row_formatted.append(col_value)
                page_formatted.append(row_formatted)

            # Ajuste manual de larguras para algumas colunas críticas (exemplo)
            # Largura padrão (automaticamente ajustada) para o restante das colunas
            colwidths = [25, 50, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20]

            print(tabulate(page_formatted, headers=headers, tablefmt='grid', colalign=colalign))
            
            # Pausa a cada página para permitir a visualização
            input("Pressione Enter para continuar...")

        # Exemplo de análise descritiva
        print("\nAnálise Descritiva:")
        desc_stats = final_df.describe().reset_index()
        print(tabulate(desc_stats, headers='keys', tablefmt='grid', floatfmt=".2f"))

        # Exportar para CSV (opcional)
        final_df.to_csv('dados_processados.csv', index=False)

except FileNotFoundError:
    print(f"Arquivo PDF não encontrado: {file_path}")
except Exception as e:
    print(f"Erro ao processar o PDF: {e}")
