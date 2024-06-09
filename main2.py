import camelot
import pandas as pd

# Carregar o arquivo PDF e extrair as tabelas
tables = camelot.read_pdf('arquivo.pdf')

# Converter as tabelas em DataFrames
dfs = []
for table in tables:
    dfs.append(table.df)

# Concatenar os DataFrames, se necessário
final_df = pd.concat(dfs)

# Exibir o DataFrame final
print(final_df)
