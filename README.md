<h1 align="center">
  <br>
  <a href="https://vantage6.ai"><img src="https://github.com/IKNL/guidelines/blob/master/resources/logos/vantage6.png?raw=true" alt="vantage6" width="400"></a>
</h1>

<h3 align=center> A privacy preserving federated learning solution</h3>

--------------------

# vantage6-toolkit
This repository is part of the [vantage6](https://vantage6.ai) solution. Vantage6 allowes to execute computations on federated datasets. This repository contains tools for algorithm development. It contains a `docker_wrapper` wrapper method which handles reading the database, input, token and writing the output. All methods that are no master method should be prefixed with `RPC_` and must be methods attached to an installed module. You can use [v6-boilerplate-py](https://github.com/iknl/v6-boilerplate-py) as a starting point for your algorithm. This package contains also a `MockClient` to test your algorithms locally.

## Installation
### Option 1: PyPi
```bash
# Install directly from pypi
pip install vantage6-toolkit
```
### Option 2: From this repository
```bash
# Clone repository
git clone https://github.com/iknl/vantage6-toolkit

# Go into the repository
cd vantage6

# install vantage6 and dependencies
pip install -e .
```

## Usage
The package contains two clients: 1) the `ClientContainerProtocol` which is used by master containers, and 2) the `MockClientProtocol` which can be used to test you algorithm locally. The `MockClientProtocol is initialized as:
```Python
from vantage6.tools.mock_client import ClientMockProtocol

# The first argument is a list consisting of a list of csv-file paths, the second
# argument is the module in which the `def` are found (at root level) that the
# algorithm can use.
client = ClientMockProtocol(["local/data-A.csv", "local/data-B.csv"], "v6-boilerplate-py")
```

The `ClientContainerProtocol` is initialized as:
```python
import os

from vantage6.tools.container_client import ClientContainerProtocol

# token is a valid JWT-token, generated on the server for this specific task
# in the docker_wrapper (see docker_wrapper.py) these are provided as an
# argument `token`.
client = ClientContainerProtocol(
    token,
    host=os.environ["HOST"],
    port=os.environ["PORT"],
    path=os.environ["API_PATH"]
)
```

Then the client can be used to create new (sub-)tasks and retrieve the results. For example if we want to run a the `master` method from the `v6-boilerplate` module. (Note that usually a master method is only invoked by a user and not by a container, however for testing purposes, using `MockClientProtocol`, this can be useful).

```Python
# collect organizations that are part of this organization. The collaboration
# and algorithm-image are derived from the JWT-token that the container uses to
# communicate with the server.
organizations = client.get_organizations_in_my_collaboration()
ids = [organization["id"] for organization in organizations]

# task = client.create_new_task({"method":"some_example_method"}, ids)
# results = client.get_results(task.get("id"))
master_task = client.create_new_task({"master": 1, "method":"master"}, [ids[0]])
results = client.get_results(task.get("id"))
print(results)

# Result should be something that looks like:
# [
#   {'id': 999, 'result': '{"Age": {"F": 31.142857142857142, "M": 36.90909090909091}}'},
#   {'id': 999, 'result': '{"Age": {"F": 31.142857142857142, "M": 36.90909090909091}}'}
# ]

```
## Read more
See the [documentation](https://docs.vantage6.ai/) for detailed instructions on how to install and use the server and nodes.

------------------------------------
> [vantage6](https://vantage6.ai)