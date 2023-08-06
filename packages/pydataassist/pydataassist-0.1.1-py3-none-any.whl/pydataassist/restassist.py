"""This is module to support encryption."""
import json
from typing import Any
from typing import Optional

import requests
from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import from_json
from pyspark.sql.types import StringType

from pydataassist.sparkassist import get_spark_schema_from_json_response


def call_api(
    api_url: str,
    method: str = "GET",
    headers: Optional[dict[str, Any]] = None,
    data: Optional[str] = None,
    response_format: str = "json",
) -> Any:
    """Call an API and return the response as a dictionary.

    Args:
        api_url (str): _description_
        method (str): _description_. Defaults to "GET".
        headers (dict[str, Any], optional): _description_. Defaults to {}.
        data (str): _description_. Defaults to "".
        response_format (str): _description_. Defaults to "json".

    Raises:
        ValueError: _description_

    Returns:
        Any: _description_
    """
    # Make a request to the API
    response = requests.request(method, api_url, headers=headers, data=data)

    # Parse the response content based on the specified format
    if response_format == "json":
        result = json.loads(response.content)
    elif response_format == "text":
        result = response.text
    elif response_format == "binary":
        result = response.content.decode()
    else:
        raise ValueError("Invalid response format specified")
    return result


def api_to_df(
    api_url: str,
    method: str = "GET",
    headers: Optional[dict[str, Any]] = None,
    data: Optional[str] = None,
    response_format: str = "json",
) -> DataFrame:
    """_summary_.

    Args:
        api_url (str): _description_
        method (str): _description_. Defaults to "GET".
        headers (dict[str, Any], optional): _description_. Defaults to {}.
        data (str): _description_. Defaults to "".
        response_format (str): _description_. Defaults to "json".

    Raises:
        ValueError: _description_

    Returns:
        DataFrame: _description_
    """
    # Make a request to the API
    response = requests.request(method, api_url, headers=headers, data=data)

    # Parse the response content based on the specified format
    if response_format == "json":
        data = json.loads(response.content)
        print(data)
    elif response_format == "text":
        data = response.text
    elif response_format == "binary":
        data = response.content.decode()
    else:
        raise ValueError("Invalid response format specified")

    # Create a Spark session
    spark = SparkSession.builder.appName("API Data").getOrCreate()

    # Define the schema for the data
    schema = get_spark_schema_from_json_response(json.dumps(data))
    print(schema.simpleString())

    # Convert the response data to a Spark DataFrame
    df = spark.createDataFrame([json.dumps(data)], StringType())
    df = df.select(from_json(df[0], schema).alias("data")).select("data.*")

    return df
