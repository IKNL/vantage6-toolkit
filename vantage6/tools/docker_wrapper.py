import os
import pickle

import pandas

from vantage6.tools.dispatch_rpc import dispact_rpc
from vantage6.tools.util import info
from . import deserialization
from .exceptions import DeserializationException

_DATA_FORMAT_SEPARATOR = '.'


def docker_wrapper(module: str):
    info(f"wrapper for {module}")

    # read input from the mounted inputfile.
    input_file = os.environ["INPUT_FILE"]
    info(f"Reading input file {input_file}")

    input_data = _load_data(input_file)

    # all containers receive a token, however this is usually only
    # used by the master method. But can be used by regular containers also
    # for example to find out the node_id.
    token_file = os.environ["TOKEN_FILE"]
    info(f"Reading token file '{token_file}'")
    with open(token_file) as fp:
        token = fp.read().strip()

    data_file = os.environ["DATABASE_URI"]
    info(f"Using '{data_file}' as database")
    # with open(data_file, "r") as fp:
    data = pandas.read_csv(data_file)

    # make the actual call to the method/function
    info("Dispatching ...")
    output = dispact_rpc(data, input_data, module, token)

    # write output from the method to mounted output file. Which will be
    # transfered back to the server by the node-instance.
    output_file = os.environ["OUTPUT_FILE"]
    info(f"Writing output to {output_file}")
    with open(output_file, 'wb') as fp:
        fp.write(pickle.dumps(output))


def _load_data(input_file):
    """
    Try to read the specified data format and deserialize the rest of the stream accordingly. If this fails, assume
    the data format is pickle.

    :param input_file:
    :return:
    """
    with open(input_file, "rb") as fp:
        try:
            input_data = _read_formatted(fp)
        except DeserializationException:
            info('No data format specified. Assuming input data is pickle format')
            fp.seek(0)
            input_data = pickle.load(fp)
    return input_data


def _read_formatted(file):
    data_format = list(_read_data_format(file))
    return deserialization.deserialize(file, data_format)


def _read_data_format(file):
    """
    Try to read the prescribed data format. The data format should be specified as follows: DATA_FORMAT.ACTUAL_BYTES.
    This function will attempt to read the string before the period. It will fail if the file is not in the right
    format.

    :param file: Input file received from vantage infrastructure.
    :return:
    """

    while True:
        try:
            char = file.read(1).decode()
        except UnicodeDecodeError:
            # We aren't reading a unicode string
            raise DeserializationException('No data format specified')

        if char == _DATA_FORMAT_SEPARATOR:
            break
        else:
            yield char

    # The file didn't have a format prepended
    raise DeserializationException('No data format specified')
