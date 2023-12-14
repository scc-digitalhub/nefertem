# Library for data quality process

`nefertem` is an exetensible framework for monitoring and managing data quality processes. With `nefertem` you can define your own data quality process, run them and get the results. You can also create specific plugins that enable the use of your favourite data quality frameworks.

## Overview

`nefertem` adopt a *run* execution model. A user defines an execution *run* with a *client* that handles also the I/O storages. Every run is executed under an *experiment*, an organizational unit.

Running `nefertem` produces in-memory objects, deriving from the execution frameworks plugged-in (e.g. frictionless, ydata_profiling, etc.), a bunch of process descriptive metadata and a series of artifacts that can be persisted on various backend storage.

The typical workflow involves the configuration of the resources, of the input storages in which the resources are saved (local or remote filesystems, databases and datalakes) and the configuration of the run itself, where the user specifies the desired operations and the frameworks to be used.

Out-of-the-box `nefertem` supports the following **data quality operation**:

- Validation
- Inference
- Profiling
- Metrics

## Example

```python
import nefertem

# Set configurations
output_path = "./nefertem_run"
store = {"name": "local", "store_type": "local"}
data_resource = {
    "name": "resource_name",
    "path": "path/to/resource",
    "store": "local",
}
run_config = {
    "operation": "inference",
    "exec_config": [{"framework": "frictionless"}]
}

# Create a client and run
client = nefertem.create_client(output_path=output_path, store=[store])
with client.create_run([data_resource], run_config) as nt_run:
    nt_run.infer()
    nt_run.log_schema()
    nt_run.persist_schema()
```

## Documentation

- [Installation and requirements](./docs/01-installation.md)
- [Configuration](./docs/02-configuration.md)
- [Modules](./docs/03-modules.md)
