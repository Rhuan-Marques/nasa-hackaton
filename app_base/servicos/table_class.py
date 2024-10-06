from pydantic import BaseModel, computed_field, field_validator
from typing import Optional
from enum import Enum
import os
from functools import cached_property
import pandas as pd
import math

class ColumnType(str, Enum):
    Int = "int"
    Float = "float"
    String = "string"
    Empty = "empty"

class Column(BaseModel):
    name: str = ""
    values: list[str]|list[int]|list[float]|list[None] = []

    @field_validator('values') 
    @classmethod
    def getvalues(cls, values, other_info):
        if not values:
            raise ValueError('values cannot be empty')
        if type(values[0]) == str:
            if all([str(val).isdigit() for val in values]):
                values = [int(val) for val in values]
            elif all([val.replace(".", "", 1).isdigit() for val in values]):
                values = [float(val) for val in values]
        elif all([type(val) == float and math.isnan(val) for val in values]):
            values = [None for val in values]
        return values

    @computed_field
    def value_type(self) -> ColumnType:
        if all(not val for val in self.values):
            return ColumnType.Empty
        if type(self.values[0]) == type(None):
            return ColumnType.Empty
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
        if self.value_type == ColumnType.String or self.value_type == ColumnType.Empty:
            return None
        return sum([float(val) for val in self.values]) / len(self.values)
    
    @computed_field
    def mediana(self) -> Optional[float]:
        if self.value_type == ColumnType.String or self.value_type == ColumnType.Empty:
            return None
        sorted_values = sorted(self.values)
        mid = len(sorted_values) // 2
        if len(sorted_values) % 2 == 0:
            return (sorted_values[mid] + sorted_values[mid-1]) / 2
        return sorted_values[mid]


class Table(BaseModel):
    columns: list[Column] = []

    @field_validator('columns')
    @classmethod
    def validate_repeated_column_names(cls, columns, other_info):
        names = [column.name for column in columns]
        if len(names) != len(set(names)):
            raise ValueError('Column names must be unique')
        return columns

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
    
    # Returns the list of columns of a certain type
    @cached_property
    def numeric_columns(self) -> list[str]:
        return [column.name for column in self.columns if column.value_type == ColumnType.Int or column.value_type == ColumnType.Float]
    
    @cached_property
    def column_dict(self) -> dict[str, Column]:
        return {column.name: column for column in self.columns}
    
    @classmethod
    def from_dataframe(cls, df: pd.DataFrame) -> 'Table':
        columns = []
        for column_name in df.columns:

            column = Column(name=column_name, values=[val if type(val) == str else "" for val in df[column_name]])
            columns.append(column)
        return cls(columns=columns)