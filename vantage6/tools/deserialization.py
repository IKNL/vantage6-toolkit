import json
import pickle

_deserializers = {}


def deserialize(file, data_format):
    """
    Lookup data_format in deserializer mapping and return the associated
    :param file:
    :param data_format:
    :return:
    """
    try:
        return _deserializers[data_format.lower()](file)
    except KeyError as e:
        raise Exception(f'Deserialization of {data_format} has not been implemented.')


def deserializer(data_format):
    """
    Register function as deserializer by adding it to the `_deserializers` map with key `data_format`.

    :param data_format:
    :return:
    """

    def decorator_deserializer(func):
        # Register deserialization function
        _deserializers[data_format] = func

        # Return function without modifications so it can also be run without retrieving it from `_deserializers`.
        return func

    return decorator_deserializer


@deserializer('json')
def deserialize_json(file):
    return json.load(file)


@deserializer('pickle')
def deserialize_pickle(file):
    return pickle.load(file)
