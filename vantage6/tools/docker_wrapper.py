import os
import json
import csv

from vantage6.tools.dispatch_rpc import dispact_rpc
from vantage6.tools.util import info


def docker_wrapper(module: str):
    info(f"wrapper for {module}")

    # read input from the mounted inputfile.
    input_file = os.environ["INPUT_FILE"]
    info(f"Reading input file {input_file}")
    with open(input_file) as fp:
        input_data = json.loads(fp.read())

    # all containers receive a token, however this is usually only
    # used by the master method. But can be used by regular containers also
    # for example to find out the node_id.
    token_file = os.environ["TOKEN_FILE"]
    info(f"Reading token file '{token_file}'")
    with open(token_file) as fp:
        token = fp.read().strip()

    data_file = os.environ["DATABASE_URI"]
    info(f"Using '{data_file}' as database")
    with open(data_file, "r") as fp:
        data = csv.reader(fp)

    # make the actual call to the method/function
    info("Dispatching ...")
    output = dispact_rpc(data, input_data, module, token)

    # write output from the method to mounted output file. Which will be
    # transfered back to the server by the node-instance.
    output_file = os.environ["OUTPUT_FILE"]
    info(f"Writing output to {output_file}")
    with open(output_file, 'w') as fp:
        fp.write(json.dumps(output))
