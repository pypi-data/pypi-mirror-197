"""This is module to support encryption."""
import json
from typing import Any

from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import from_json
from pyspark.sql.types import ArrayType
from pyspark.sql.types import BooleanType
from pyspark.sql.types import DoubleType
from pyspark.sql.types import IntegerType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


def get_spark_schema_from_json_response(json_response: str) -> StructType:
    """Extract the schema from a JSON response and return it as a Spark StructType.

    Args:
        json_response (str): The JSON response
            from which to extract the schema.

    Returns:
        A Spark StructType representing the schema of the JSON data.
    """
    # Convert the JSON response to a Python dictionary
    response_dict = json.loads(json_response)

    # Create a list of StructFields based on the keys and value types in the dictionary
    fields = []
    for key, value in response_dict.items():
        if isinstance(value, str):
            fields.append(StructField(key, StringType(), True))
        elif isinstance(value, int):
            fields.append(StructField(key, IntegerType(), True))
        elif isinstance(value, float):
            fields.append(StructField(key, DoubleType(), True))
        elif isinstance(value, bool):
            fields.append(StructField(key, BooleanType(), True))
        elif isinstance(value, list):
            # If the value is a list, get the element type
            # and create an ArrayType StructField
            element_type = get_element_type(value)
            fields.append(StructField(key, ArrayType(element_type, True), True))
        else:
            # If the value is a dictionary, recursively create a StructType StructField
            sub_fields = get_spark_schema_from_json_response(json.dumps(value)).fields
            fields.append(StructField(key, StructType(sub_fields), True))

    # Create a StructType schema using the list of StructFields
    schema = StructType(fields)

    return schema


def get_element_type(list_obj: Any) -> Any:
    """_summary_.

    Args:
        list_obj (Any): _description_

    Returns:
        Any: _description_
    """
    # Get the element type of a list by recursively checking its elements
    if isinstance(list_obj[0], str):
        return StringType()
    elif isinstance(list_obj[0], int):
        return IntegerType()
    elif isinstance(list_obj[0], float):
        return DoubleType()
    elif isinstance(list_obj[0], bool):
        return BooleanType()
    elif isinstance(list_obj[0], list):
        # If the element is a list, recursively get its element type
        return ArrayType(get_element_type(list_obj[0]), True)
    else:
        # If the element is a dictionary, recursively create a StructType
        sub_fields = get_spark_schema_from_json_response(json.dumps(list_obj[0])).fields
        return StructType(sub_fields)


def get_spark_df_from_json(json_data: str) -> DataFrame:
    """_summary_.

    Args:
        json_data (str): _description_

    Returns:
        DataFrame: _description_
    """
    # Create a Spark session
    spark = SparkSession.builder.appName("API Data").getOrCreate()

    # Define the schema for the data
    schema = get_spark_schema_from_json_response(json_response=json_data)

    # Convert the response data to a Spark DataFrame
    df = spark.createDataFrame([json.dumps(json_data)], StringType())
    df = df.select(from_json(df[0], schema).alias("data")).select("data.*")

    return df
