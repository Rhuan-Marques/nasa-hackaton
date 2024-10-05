# Importando bibliotecas necessárias
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregando o arquivo CSV
# Aqui, você pode usar o caminho correto do arquivo ou ler de uma string diretamente se estiver em outro ambiente
df = pd.read_csv('Datasets/Dataset1/a_OSD-379_transcription-profiling_rna-sequencing-(rna-seq)_Illumina NovaSeq.csv', sep='\t')

# Remover colunas desnecessárias para a visualização
df_clean = df[['Sample Name', 'Parameter Value[QA Score]', 'Parameter Value[Fragment Size]', 
               'Parameter Value[Read Depth]', 'Parameter Value[rRNA Contamination]']].copy()

df_clean['Parameter Value[QA Score]'] = pd.to_numeric(df_clean['Parameter Value[QA Score]'], errors='coerce')
df_clean['Parameter Value[Fragment Size]'] = pd.to_numeric(df_clean['Parameter Value[Fragment Size]'], errors='coerce')
df_clean['Parameter Value[Read Depth]'] = pd.to_numeric(df_clean['Parameter Value[Read Depth]'], errors='coerce')
df_clean['Parameter Value[rRNA Contamination]'] = pd.to_numeric(df_clean['Parameter Value[rRNA Contamination]'], errors='coerce')

# Gráfico de barras: Comparação do QA Score por Sample Name
plt.figure(figsize=(10,6))
sns.barplot(x='Sample Name', y='Parameter Value[QA Score]', data=df_clean)
plt.xticks(rotation=90)
plt.title('QA Score por Amostra')
plt.savefig('qa_score_por_amostra.png')  # Salvando o gráfico como imagem
plt.close()

# Histograma: Distribuição de Fragment Size
plt.figure(figsize=(10,6))
sns.histplot(df_clean['Parameter Value[Fragment Size]'], bins=20, kde=True)
plt.title('Distribuição do Tamanho dos Fragmentos')
plt.xlabel('Tamanho do Fragmento (base pair)')
plt.ylabel('Frequência')
plt.savefig('distribuicao_fragment_size.png')  # Salvando o gráfico como imagem
plt.close()

# Scatter Plot: Relação entre QA Score e Fragment Size
plt.figure(figsize=(10,6))
sns.scatterplot(x='Parameter Value[QA Score]', y='Parameter Value[Fragment Size]', hue='Sample Name', data=df_clean)
plt.title('Relação entre QA Score e Fragment Size')
plt.xlabel('QA Score')
plt.ylabel('Fragment Size (base pair)')
plt.savefig('relacao_qa_score_fragment_size.png')  # Salvando o gráfico como imagem
plt.close()

# Boxplot: Contaminação de rRNA entre amostras
plt.figure(figsize=(10,6))
sns.boxplot(x='Sample Name', y='Parameter Value[rRNA Contamination]', data=df_clean)
plt.xticks(rotation=90)
plt.title('Contaminação de rRNA por Amostra')
plt.savefig('contaminacao_rrna.png')  # Salvando o gráfico como imagem
plt.close()
