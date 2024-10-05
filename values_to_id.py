import json

ID_TO_VALUE = {}

def main():

    filename = "outputs/parser/a_OSD-379_transcription-profiling_rna-sequencing-(rna-seq)_Illumina NovaSeq.csv"

    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    values = [line.split(",") for line in lines[1:]]

    for idx_column in range(len(values[0])):
        vals_on_collum = {}
        for idx_row in range(len(values)):
            val = values[idx_row][idx_column]
            if val not in vals_on_collum.keys():
                ID_TO_VALUE[len(ID_TO_VALUE)+1] = val
                vals_on_collum[val] = True
    
    print(json.dumps(ID_TO_VALUE))

    

if __name__ == "__main__":
    main()
