import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('Datasets/Dataset1/s_OSD-379.csv', delimiter='\t')

print("Primeiras linhas do DataFrame:")
print(df.head())

colunas_para_remover = ['Term Source REF', 'Term Accession Number']

colunas_existentes = [col for col in colunas_para_remover if col in df.columns]
df.drop(columns=colunas_existentes, inplace=True)

df.fillna('N/A', inplace=True)

print("\nInformações do DataFrame após limpeza:")
print(df.info())

colunas_importantes = ['Source Name', 'Sample Name', 'Characteristics[Organism]', 
                       'Characteristics[Sex]', 'Factor Value[Age]', 'Factor Value[Duration]']
df_selecionado = df[colunas_importantes]

print("\nDataFrame selecionado:")
print(df_selecionado.head())

sns.set(style="whitegrid")

plt.figure(figsize=(12, 6))
sns.countplot(data=df_selecionado, x='Factor Value[Age]', palette='viridis')
plt.title('Distribuição de Idades')
plt.xlabel('Idade (semanas)')
plt.ylabel('Contagem')
plt.xticks(rotation=45)
plt.show()

df_selecionado.to_csv('csv_limpo.csv', index=False)
print("\nDataFrame limpo salvo como 'csv_limpo.csv'.")