import camelot
import pandas as pd

file_path = "TesteDataFrame.pdf"

try:
    tables = camelot.read_pdf(file_path, pages='all', flavor='stream')

    if not tables:
        print("Nenhuma tabela encontrada no arquivo PDF.")
    else:
        dfs = [table.df for table in tables]
        final_df = pd.concat(dfs, ignore_index=True)

        first_row = final_df.iloc[0]
        if any(pd.notna(first_row)):
            final_df.columns = first_row
            final_df = final_df.iloc[1:].reset_index(drop=True)
        else:
            num_columns = len(final_df.columns)
            final_df.columns = [f"Coluna{i+1}" for i in range(num_columns)]

        print(final_df)

except Exception as e:
    print(f"Erro ao processar o PDF: {e}")


