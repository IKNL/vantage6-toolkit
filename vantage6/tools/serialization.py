import pickle

import json
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
    info(f'Serializing type {type(data)} to json')

    if isinstance(data, pd.DataFrame) | isinstance(data, pd.Series):
        return _serialize_pandas(data)

    return _default_serialization(data)


def _default_serialization(data):
    info('Using default json serialization')
    return json.dumps(data).encode()


def _serialize_pandas(data):
    info('Running pandas json serialization')
    return data.to_json().encode()


@serializer('pickle')
def serialize_to_pickle(data):
    info('Serializing to pickle')
    return pickle.dumps(data)
