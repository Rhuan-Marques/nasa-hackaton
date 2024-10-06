import pandas as pd

def load_data(uploaded_file, delimiter=','):
    try:
        # Salvar o arquivo para debug
        with open("uploaded_file.csv", "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Ler o arquivo com o delimitador especificado
        df = pd.read_csv("uploaded_file.csv", delimiter=delimiter)
        print("DataFrame head:", df.head())  # Para verificar os dados carregados
        return df
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None
