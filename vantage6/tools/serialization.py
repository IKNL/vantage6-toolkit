import jsonpickle
import pandas as pd

from vantage6.tools.util import info

_serializers = {}


def serialize(data, data_format):
    """
    Look up serializer for `data_format` and use this to serialize `data`.
    :param data:
    :param data_format:
    :return:
    """
    return _serializers[data_format.lower()](data)


def serializer(data_format):
    """
    Register function as deserializer by adding it to the `_deserializers` map with key `data_format`.

    :param data_format:
    :return:
    """

    def decorator_serializer(func):
        # Register deserialization function
        _serializers[data_format] = func

        # Return function without modifications so it can also be run without retrieving it from `_deserializers`.
        return func

    return decorator_serializer


@serializer('json')
def serialize_to_json(data):
    info(f'Serializing type {type(data)}')

    if isinstance(data, pd.DataFrame) | isinstance(data, pd.Series):
        return serialize_pandas(data)

    return default_serialization(data)


def default_serialization(data):
    info('Using default serialization')
    return jsonpickle.encode(data, unpicklable=True)


def serialize_pandas(data):
    info('Running pandas serialization')
    return data.to_json()
