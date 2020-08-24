"""
Class DataFormat

This Enum contains all the possible dataformats that can be used to serialize or deserialize the data to and from the
algorithm wrapper.

When serialization to an additional data format is implemented it should be added here.
"""
from enum import Enum


# TODO: Should ideally be shared with the client as well
class DataFormat(Enum):
    JSON = 'json'
    PICKLE = 'pickle'
