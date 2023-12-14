
# Authentication

`nefertem` allows passing credentials to backend storages through the **input store** configuration.
The configuration is a `dict` object specific for the following backend storages:

* **s3**
* **remote**
* **sql**

## S3

The *s3* store requires *endpoint_url*, *aws_access_key_id* and *aws_secret_access_key*. It requires also a *bucket_name* to get the data from.

```python
   store_cfg = {
       "endpoint_url": "http://host:port/",
       "aws_access_key_id": "acc_key",
       "aws_secret_access_key": "sec_key",
       "bucket_name": "bucket_name"
   }
```

## Remote

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

## SQL

An SQL store requires a set of credentials to connect to the database and the specific driver to use.

```python

   store_cfg = {
       "driver": "driver", # e.g. mysql, postgresql, etc.
       "host": "host",
       "port": "port",
       "user": "user",
       "password": "password",
       "database": "database"
   }
```
