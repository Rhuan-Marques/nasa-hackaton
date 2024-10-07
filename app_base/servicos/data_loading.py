import pandas as pd

def load_data(lines: list[str], delimiter=','):
    try:
        print(f'Lines: {" ||| ".join(lines)}')
        # Salvar o arquivo para debug
        with open("uploaded_file.csv", "w") as f:
            f.write("\n".join(lines))

        # Ler o arquivo com o delimitador especificado
        df = pd.read_csv("uploaded_file.csv", delimiter=delimiter)
        print("DataFrame head:", df.head())  # Verificar dados carregados
        return df
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None
