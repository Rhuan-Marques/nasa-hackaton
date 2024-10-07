import pandas as pd

def process_data(df):
    """
    Process the DataFrame to clean and prepare data for analysis and visualization.
    
    Parameters:
    df: DataFrame containing the raw data
    
    Returns:
    DataFrame: Cleaned DataFrame for visualization and analysis
    """
    # Remover colunas que não são úteis para visualizações ou análise
    df_clean = df.copy()

    # Convertendo colunas relevantes para numéricas, lidando com erros
    for column in df_clean.select_dtypes(include=['object']).columns:
        df_clean[column] = pd.to_numeric(df_clean[column], errors='coerce')
    
    # Remover linhas com valores ausentes
    df_clean.dropna(inplace=True)
    
    return df_clean
