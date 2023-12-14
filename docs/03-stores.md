
# Stores

A store is an object that `nefertem` uses to interact with resources, artifacts and metadata. There are two kinds of stores, one for input data, and the other for output data. The input store is used to fetch artifacts from various backends, while the output store is used to persist artifacts and metadata.

## Output Store

The outputh store is configured by specifying an `outputh_path`:

```python

   import nefertem

   output_path = "./nt_runs"
```

The output path **MUST** be a local path. `nefertem` uses this path to store output artifacts and metadata.

## Input Store

Input stores are configured using a `dict` object structured this way:

* `name`, required, identifier of the store
* `store_type`, required, specific store type to be instantiated. See below for supported store types
* `config`, optional, use to configure credentials, please see `Authentication <./authentication.md>`_ documentation for more information

For example:

```python

   import nefertem

   store = {"name": "local", "store_type": "local"}
```

`nefertem` supports the following store types:

* *local*
* *s3*
* *sql*
* *remote* (as http)
