
Client
======

A ``Client`` is an high level interface that allows an user to interact with backend storages and creates runs associated within an ``experiment``.
You can create a ``Client`` this way:

```python

   import nefertem

   output_path = "./nefertem_run"
   store = {"name": "local", "store_type": "local"}

   client = nefertem.create_client(output_path=output_path, store=[store])

The ``output_path`` is the path where the ``Client`` will store the runs and all the output files (metadata, reports, etc.) and the ``store`` is a dictionary that contains the information of the backend storage.
