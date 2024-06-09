import tabula
import pandas as pd

# Carregar o arquivo PDF
file_path = "caminho/para/o/arquivo.pdf"

# Extrair tabelas do PDF
tables = tabula.read_pdf(file_path, pages='all')

# Converter as tabelas em DataFrames
dfs = []
for table in tables:
    df = pd.DataFrame(table)
    dfs.append(df)

final_df = pd.concat(dfs, ignore_index=True)

print(final_df)