
# Client

A `Client` is an high level interface that allows an user to interact with backend storages and creates `runs` associated within an `experiment`. It is the starting point of the library.
You can create a `Client` this way:

```python

   import nefertem

   output_path = "./nefertem_run"
   store = {"name": "local", "store_type": "local"}

   client = nefertem.create_client(output_path=output_path, store=[store])
```

## Client parameters

- `output_path`: a string path where the `Client` will store the runs and all the output files (metadata, reports, etc.).
- `store`: a list of dictionary store configurstions.
