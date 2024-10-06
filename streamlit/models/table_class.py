from pydantic import BaseModel, computed_field, field_validator
from typing import Optional
from enum import Enum
import os

class ColumnType(str, Enum):
    Int = "int"
    Float = "float"
    String = "string"

class Column(BaseModel):
    name: str = ""
    values: list[str|int|float] = []

    @field_validator('values') 
    @classmethod
    def getvalues(cls, values, other_info):
        if not values:
            raise ValueError('values cannot be empty')
        types = set([type(val) for val in values])
        if len(types) > 1:
            raise ValueError('values must be of the same type')
        if type(values[0]) not in [str, int, float]:
            raise ValueError('values must be of type str, int or float')
        if type(values[0]) == str:
            if all([str(val).isdigit() for val in values]):
                values = [int(val) for val in values]
            else:
                try:
                    values = [float(val) for val in values]
                except ValueError:
                    pass
        
        return values

    @computed_field
    def value_type(self) -> ColumnType:
        if type(self.values[0]) == int:
            return ColumnType.Int
        if type(self.values[0]) == float:
            return ColumnType.Float
        return ColumnType.String  
    
    @computed_field
    def moda(self) -> str|int|float:
        return max(set(self.values), key = self.values.count)
    
    @computed_field
    def media(self) -> Optional[float]:
        if self.value_type == ColumnType.String:
            return None
        return sum([float(val) for val in self.values]) / len(self.values)
    
    @computed_field
    def mediana(self) -> Optional[float]:
        if self.value_type == ColumnType.String:
            return None
        sorted_values = sorted(self.values)
        mid = len(sorted_values) // 2
        if len(sorted_values) % 2 == 0:
            return (sorted_values[mid] + sorted_values[mid-1]) / 2
        return sorted_values[mid]


class Table(BaseModel):
    columns: list[Column] = []

    @classmethod
    def from_csv(cls, filename: str) -> 'Table':
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        names = lines[0].split(",")
        values = [line.split(",") for line in lines[1:]]
        columns = []
        for idx_column in range(len(names)):
            column = Column(name=names[idx_column], values=[values[idx_row][idx_column] for idx_row in range(len(values))])
            columns.append(column)

        return cls(columns=columns)


def create_table_object(filename: str) -> Table:
    table = Table.from_csv(filename)

    os.makedirs('outputs/table_objects', exist_ok=True)
    output_path = os.path.join('outputs/table_objects', os.path.basename(filename).split(".")[0] + ".json")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(table.model_dump_json())
    return
    

if __name__ == "__main__":
    create_table_object("outputs/parser/a_OSD-379_transcription-profiling_rna-sequencing-(rna-seq)_Illumina NovaSeq.csv")
