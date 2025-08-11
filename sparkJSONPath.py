from jsonpath_ng import parse
from pyspark.sql.functions import pandas_udf, udf
from pyspark.sql.types import StringType, ArrayType, StructType, Row
import pandas as pd
from typing import Union, Callable


# Get the first match of a JSONPath expression in a StructType column
@udf(StringType())
def get_value(struct_dict: Union[Row,list], path: str) -> str:
    """
    Evaluate JSONPath on a StructType (represented as a Python dict) and return the first string match
    or None if no match.
    """
    if isinstance(struct_dict, Row):
        struct_dict = struct_dict.asDict(recursive=True)
    elif isinstance(struct_dict, list):
        struct_dict = [row.asDict(recursive=True) for row in struct_dict]
        
    if not struct_dict or not path:
        return None
    json_expr = parse(path)
    matches = [match.value for match in json_expr.find(struct_dict)]
    return str(matches[0]) if matches else None


# Get all matches of a JSONPath expression in a StructType column
@udf(ArrayType(StringType()))
def get_all_values(struct_dict: Union[Row,list], path: str) -> list:
    """
    Evaluate JSONPath on a StructType (represented as a Python dict) and return all string matches
    or an empty list if no match.
    """
    if isinstance(struct_dict, Row):
        struct_dict = struct_dict.asDict(recursive=True)
    elif isinstance(struct_dict, list):
        struct_dict = [row.asDict(recursive=True) for row in struct_dict]

    if not struct_dict or not path:
        return []
    json_expr = parse(path)
    return [str(match.value) for match in json_expr.find(struct_dict)]


def makeStructUpdateUDF(jsonpath: str, func: Callable, schema: StructType) -> Callable:
    """
    Creates a Spark UDF to update a StructType column based on a JSONPath expression.

    :param jsonpath: The JSONPath expression to select parts of the struct to update.
    :param func: func should take 3 arguments: the value, the parent object, and the field/index, return the new value.
    :param schema: The schema (StructType) of the output column.
    :return: A Spark UDF that can be applied to a column.
    """
    jsonpath_expr = parse(jsonpath)
    def _update_worker(struct_obj):
        if struct_obj is None:
            return None
        # Convert Row to dict, perform update, and return dict
        # Spark will convert the dict back to a Row based on the schema
        obj_dict = struct_obj.asDict(recursive=True)
        jsonpath_expr.update(obj_dict, func)

        return obj_dict

    return udf(_update_worker, schema)
