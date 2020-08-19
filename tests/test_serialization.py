import pickle

from pytest import mark

from vantage6.tools import serialization
import pandas as pd

JSON = 'json'


@mark.parametrize("data,target", [
    # Default serialization
    ([1, 2, 3], '[1, 2, 3]'),
    ('hello', '"hello"'),
    ({'hello': 'goodbye'}, '{"hello": "goodbye"}'),

    # Pandas serialization
    (pd.DataFrame([[1, 2, 3]], columns=['one', 'two', 'three']), '{"one":{"0":1},"two":{"0":2},"three":{"0":3}}'),
    (pd.Series([1, 2, 3]), '{"0":1,"1":2,"2":3}')
])
def test_json_serialization(data, target):
    result = serialization.serialize(data, JSON)

    assert target == result.decode()


@mark.parametrize("data", [
    ({'key': 'value'}),
    (123),
    ([1, 2, 3]),
])
def test_pickle_serialization(data):
    pickled = serialization.serialize(data, 'pickle')

    assert data == pickle.loads(pickled)


def test_pickle_serialization_pandas():
    data = pd.DataFrame([1, 2, 3])
    pickled = serialization.serialize(data, 'pickle')

    pd.testing.assert_frame_equal(data, pickle.loads(pickled))
