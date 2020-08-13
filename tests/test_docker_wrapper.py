import json
import pickle
from unittest.mock import patch

import pandas as pd
from pytest import raises

from vantage6.tools import docker_wrapper
from vantage6.tools.exceptions import DeserializationException

MODULE_NAME = 'algorithm_module'
DATA = 'column1,column2\n1,2'
TOKEN = 'This is a fake token'
INPUT_PARAMETERS = {'method': 'hello_world'}
JSON = 'json'
SEPARATOR = '.'


def test_old_pickle_input_wrapper(tmp_path):
    input_file = tmp_path / 'input.pkl'

    with input_file.open('wb') as f:
        pickle.dump(INPUT_PARAMETERS, f)

    run_docker_wrapper(tmp_path, input_file)


def test_json_input_without_format_raises_deserializationexception(tmp_path):
    input_file = tmp_path / 'input.json'

    with input_file.open('wb') as f:
        f.write(json.dumps(INPUT_PARAMETERS).encode())

    with raises(DeserializationException):
        run_docker_wrapper(tmp_path, input_file)


def test_json_input_with_format_succeeds(tmp_path):
    input_file = tmp_path / 'input.txt'

    with input_file.open('wb') as f:
        f.write(f'JSON{SEPARATOR}'.encode())
        f.write(json.dumps(INPUT_PARAMETERS).encode())

    run_docker_wrapper(tmp_path, input_file)


def run_docker_wrapper(tmp_path, input_file):
    db_file = tmp_path / 'db_file.csv'
    token_file = tmp_path / 'token.txt'
    output_file = tmp_path / 'output_file.pkl'

    db_file.write_text(DATA)
    token_file.write_text(TOKEN)

    with patch('vantage6.tools.docker_wrapper.os') as mock_os:
        mock_os.environ = {
            'INPUT_FILE': input_file,
            'TOKEN_FILE': token_file,
            'OUTPUT_FILE': output_file,
            'DATABASE_URI': db_file
        }

        docker_wrapper.docker_wrapper(MODULE_NAME)

    with output_file.open('rb') as f:
        result = pickle.load(f)

        print(result)

        target = pd.DataFrame([[1, 2]], columns=['column1', 'column2'])
        pd.testing.assert_frame_equal(target, result)


def _prepare_input(input_, input_file):
    input_file.write(input_.encode())
    input_file.seek(0)
