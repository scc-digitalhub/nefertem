
Stores
======

A store is an object that *nefertem* uses to interact with resources, artifacts and metadata.
They can be configured using a specific ``StoreConfig`` object that accepts the following parameters:


* ``name``, required, identifier of the store
* ``type``, required, specific store type to be instantiated
* ``uri``, required, URI location of artifacts/metadata
* ``title``, optional, human readable description for the store
* ``isDefault``, optional, set an ``InputStore`` as the one where artifact are persisted, ignored by ``OutputStore``
* ``config``, optional, use to configure credentials, please see `Authentication <./authentication.md>`_ documentation for more information

There are two types of store:


* ``OutputStore``
* ``InputStore``

OutputStore
-------------

The ``OutputStore`` is used by the library to log metadata into a specified backend.

Example configuration:

.. code-block:: python

   import nefertem as nt

   METADATA_STORE = nt.StoreConfig(title="Local Metadata Store",
                                   type="local",
                                   name="local_md",
                                   uri="./ntruns")

In this case we create a *local* ``OutputStore`` that will log metadata locally.
``OutputStore`` supports the following types:


* *local*
* *http* (DigitalHub store)

InputStore
-------------

The ``InputStore`` is used by the library to fetch and persist artifact from various backend. It is configured like a ``OutputStore``.
If you configure more than one ``InputStore``, at least one must be set as ``isDefault``.
``InputStore`` supports the following types:


* *local*
* *s3*
* *azure*
* *ftp*
* *http* (Doesn't support artifact persistence)
* *sql* (Doesn't support artifact persistence)
* *odbc* (Doesn't support artifact persistence)
