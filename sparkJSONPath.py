from jsonpath_ng import parse
from pyspark.sql.functions import pandas_udf, udf
from pyspark.sql.types import StringType, ArrayType, StructType
import pandas as pd
from typing import Union, Callable

# Get the first match of a JSONPath expression in a StructType column
@pandas_udf(StringType())
def get_value(root:Union[pd.Series,pd.DataFrame], path: pd.Series) -> pd.Series:
    """
    Evaluate JSONPath on each StructType (represented as a Python dict) and return the first string match
    or None if no match.
    """
    compiled_exprs = {}
    results = []

    row_iterator = (row._asdict() for row in root.itertuples(index=False)) if isinstance(root, pd.DataFrame) else root

    for struct_dict, expr in zip(row_iterator, path):
        # compile JSONPath expression once per unique path
        json_expr = compiled_exprs.get(expr)
        if json_expr is None:
            json_expr = parse(expr)
            compiled_exprs[expr] = json_expr

        matches = [match.value for match in json_expr.find(struct_dict)]

        if matches:
            results.append(str(matches[0]))
        else:
            results.append(None)

    return pd.Series(results)


# Get all matches of a JSONPath expression in a StructType column
@pandas_udf(ArrayType(StringType()))
def get_all_values(root:Union[pd.Series,pd.DataFrame], path: pd.Series) -> pd.Series:
    """
    Evaluate JSONPath on each StructType (represented as a Python dict) and return all string matches
    or an empty list if no match.
    """
    compiled_exprs = {}
    results = []

    row_iterator = (row._asdict() for row in root.itertuples(index=False)) if isinstance(root, pd.DataFrame) else root

    for struct_dict, expr in zip(row_iterator, path):
        # compile JSONPath expression once per unique path
        json_expr = compiled_exprs.get(expr)
        if json_expr is None:
            json_expr = parse(expr)
            compiled_exprs[expr] = json_expr

        matches = [str(match.value) for match in json_expr.find(struct_dict)]

        results.append(matches)

    return pd.Series(results)


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
        # The underlying structUpdate expects a function with 3 args,
        # but we want the user to provide a simple function with 1 arg.
        # This lambda bridges that gap.
        return obj_dict

    return udf(_update_worker, schema)
