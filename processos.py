nome_arquivo = 'Datasets/Dataset1/a_OSD-379_transcription-profiling_rna-sequencing-(rna-seq)_Illumina NovaSeq.csv'

# Abrir e ler o arquivo
with open(nome_arquivo, 'r') as arquivo:
    conteudo = arquivo.read()

# Imprimir o conteúdo do arquivo
print(conteudo)
