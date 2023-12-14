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

## HOW TO

- [Example](./docs/00-examples.md)

- [Installation and requirements](./docs/01-installation.md)

- [Client](./docs/02-client.md)
- [Stores](./docs/03-stores.md)
- [Authentication](./docs/04-authentication.md)
- [Dataresource](./docs/04-dataresource.md)

- [Modules](./docs/06-modules.md)
- [Validation](./docs/07-validation.md)
- [Inferece](./docs/08-inference.md)
- [Profiling](./docs/09-profiling.md)
- [Metrics](./docs/10-metrics.md)
