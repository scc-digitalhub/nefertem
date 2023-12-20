# Nefertem configuration

To execute a `nefertem` you need to perform some configuration steps. You need to define some elemets that are required by the internals of `nefertem`.

Roughly speaking, you need to define:

- **data resources** to be used in the run.
- **stores** configuration where the resources are saved.
- **client** that handles the I/O storages and the creation of runs.
- **run configuration** that contains the operations to be executed.
- according to the operations, you may need to configure the frameworks and other stuff.

## Data resources

A `DataResource` is a representation of a pyhisical or virtual tabular resource. It is defined with a `dict` object.

A basic `DataResource` must have a name, a path to the input data and a refernce to the store where it can be retrieved.
Optionally, you can add a `table_schema` to describe the data structure, a `package` name to group the resources, a `title` and a `description` to enrich the metadata.

```python
resource = {
    "name": "res-name",
    "path": "path-to-data",
    "store": "store-name",
    "table_schema": "path to a data schema or an embedded schema",
    "package": "name of the package to which the resource belongs",
    "title": "human readable name",
    "description": "description of the resource"
}
```

At runtime, if a run try to fetch a `DataResource` from a `Store` that is not passed to the `Client` constructor, the program will raise a `StoreError`.

## Stores

A store is an object that `nefertem` uses to interact with resources, artifacts and metadata. There are two kinds of stores, one for input data, and the other for output data. The input store is used to fetch artifacts from various backends, while the output store is used to persist artifacts and metadata.

### Output Store

The outputh store is configured by specifying an `outputh_path`:

```python
output_path = "./nt_runs"
```

The output path **MUST** be a local path. `nefertem` uses this path to store output artifacts and metadata.

### Input Store

Input stores are configured using a `dict` object structured this way:

- `name`, required, identifier of the store
- `store_type`, required, specific store type to be instantiated. See below for supported store types
- `config`, optional, use to configure credentials, please see `Authentication <./authentication.md>`_ documentation for more information

For example:

```python
store = {"name": "local", "store_type": "local"}
```

`nefertem` supports the following store types:

- *local*
- *s3*
- *sql*
- *remote* (as http)

### Authentication

`nefertem` allows passing credentials to backend storages through the **input store** configuration.
The configuration is a `dict` object specific for the following backend storages:

#### S3

The *s3* store requires *endpoint_url*, *aws_access_key_id* and *aws_secret_access_key*. It requires also a *bucket_name* to get the data from.

```python
store_cfg = {
    "endpoint_url": "http://host:port/",
    "aws_access_key_id": "acc_key",
    "aws_secret_access_key": "sec_key",
    "bucket_name": "bucket_name"
}
```

#### Remote

There are two types of authentication for the *remote* store, basic and oauth.

The *basic* authentication requires a *username* and a *password*.

```python
store_cfg = {
    "auth": "basic",
    "user": "username",
    "password": "password"
}
```

The *oauth* requires a token provided by user.

```python
store_cfg = {
    "auth": "oauth",
    "token": "token"
}
```

#### SQL

An SQL store requires a set of credentials to connect to the database and the specific driver to use.

```python
store_cfg = {
    "driver": "driver", # e.g. postgresql+psycopg2
    "host": "host",
    "port": "port",
    "user": "user",
    "password": "password",
    "database": "database"
}
```

## Client

A `Client` is an high level interface that allows an user to interact with backend storages and creates `runs` associated within an `experiment`. It is the starting point of the library.
You can create a `Client` this way:

```python
import nefertem

output_path = "./nefertem_run"
store = {"name": "local", "store_type": "local"}

client = nefertem.create_client(output_path=output_path, store=[store])
```

### Client parameters

- `output_path`: a string path where the `Client` will store the runs and all the output files (metadata, reports, etc.).
- `store`: a list of dictionary store configurstions.

## Run

The `run` object is the main object of `nefertem`. It is the object that allows to execute operations and to log metadata and artifacts.

The `run` object is initialized with a `Client` through the method `client.create_run()`. This method accepts the following arguments:

- **resources**, a list of `DataResource` to execute the operations on.
- **run_config**, a dictionary that contains the configuration of the execution of the operations. The configuration is specific to the operation and to the framework used to execute it. See the [next documentation section](./03-modules.md) for more details.
- **experiment**, optional, a string to identify the experiment.
- **run_id**, optional, a string to identify the run.
- **overwrite**, optional, a boolean to overwrite the run if it already exists.

A run can be created this way:

```python
import nefertem

import nefertem

output_path = "./nefertem_run"
store = {"name": "local", "store_type": "local"}

client = nefertem.create_client(output_path=output_path, store=[store])

run_config = {
    "operation": "type-of-operation",
    "exec_config": [{
        "framework": "framework-to-use",
        "exec_args": { "framework-specific-config": "value" }, # Specific for the framework to use
    }],
    "parallel": False, # optional, default False
    "num_workers": 1 # optional, default 1
}

run = client.create_run(
    resources=[resource],
    run_config=run_config,
    experiment="experiment-name",
    run_id="run-id",
    overwrite=True
)
```

## Execution

Once you have created a `run` object, you can execute it as context manager:

```python
with run as r:
    # Here you can execute operations
    # specified in the run configuration
```

You can execute one type of operation at a time. For example, if you have a run configuration with two operations, one for inference and one for profiling, you need to create two runs, one for each operation.

In the [next section](./03-modules.md) you can find the documentation of the operations and the frameworks supported by `nefertem`.
