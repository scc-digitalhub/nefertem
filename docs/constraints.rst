
### Constraints


A `Constraint` is a rule that resource must fit to be considered valid.
You can define as many `Constraint` as you want, and *nefertem* will pass them to the desired framework of validation.

`Constraints` share the following parameters

- *name*, identifier for the constraint
- *title*, optional, human readable version of the identifier
- *resources*, targeted LIST of resources
- *weight*, optional, importance of an eventual error

### Constraint types

- `Frictionless`_
- `Frictionless schema`_
- `DuckDB`_
- `SQLAlchemy`_
- `Evidently`_

#### Frictionless

The parameters to define a `ConstraintFrictionless` are the following:

- *field*, specified targeted field
- *fieldType*, specified targeted field type
- *constraint*, frictionless constraint

  - *format*
  - *type*
  - *required*
  - *unique*
  - *minLength*
  - *maxLength*
  - *minimum*
  - *maximum*
  - *pattern*
  - *enum*

- *value*, value expeted

Example:

```python

   import nefertem as nt

   # Artifact Store
   STORE_LOCAL_01 = nt.StoreConfig(name="local",
                                   type="local",
                                   uri="./ntruns",
                                   isDefault=True)


   # Data Resource
   RES_LOCAL_01 = nt.DataResource(path="path-to-data",
                                  name="example-resource",
                                  store="local")


   # Example constraint. We expect that the values of the
   #  specified field have a maximum lenght of 11 characters.
   CONSTRAINT_01 = nt.ConstraintFrictionless(title="Example frictionless constraint",
                                             name="example-const",
                                             resources=["example-resource"],
                                             field="field-to-validate",
                                             fieldType="string",
                                             constraint="maxLength",
                                             value=11,
                                             weight=5)
```

#### Frictionless schema
-------------------

The parameters to define a `ConstraintFullFrictionless` are the following:


- *schema*, a dictionary (or a frictionless `Schema`), formatted as `frictionless Schema`.

Example:

```python

   import nefertem as nt

   # Artifact Store
   STORE_LOCAL_01 = nt.StoreConfig(name="local",
                                   type="local",
                                   uri="./ntruns",
                                   isDefault=True)


   # Data Resource
   RES_LOCAL_01 = nt.DataResource(path="path-to-data",
                                  name="example-resource",
                                  store="local")

   SCHEMA_01 = {
     "fields": [
       {"name":"col1", "type": "string"},
       {"name":"col2", "type": "integer"},
       {"name":"col3", "type": "float"},
     ]
   }

   # Example constraint. We will pass to a validator a full frictionless schema.
   CONSTRAINT_01 = nt.ConstraintFullFrictionless(title="Example frictionless_schema constraint",
                                                 name="example-const",
                                                 resources=["example-resource"],
                                                 tableSchema=SCHEMA_01,
                                                 weight=5)

#### DuckDB
------

The parameters to define a `ConstraintDuckDB` are the following:


- *query*, an SQL query that will be executed on the resources

  * Please note that the query require some precautions

    * When you select from a resource, the resource must be written lowercase
    * The name of the resource where you select from must be in the list of resources passed to the constraint

- *expect*, expected tipology of result

  - *empty* (only for *check = rows*)
  - *non-empty* (only for *check = rows*)
  - *exact*
  - *range*
  - *minimum*
  - *maximum*

- *value*, value expected

  * Please note that when *expect* is equals to *range*, this parameter accepts a string formatted as follows

    - "(num1, num2)" upper exclusive, lower exclusive
    - "(num1, num2]" upper exclusive, lower inclusive
    - "[num1, num2)" upper inclusive, lower exclusive
    - "[num1, num2]" upper inclusive, lower inclusive

  - *minimum* and *maximum* are inclusive

- *check*, tipology of result to evaluate

  - *rows* check number of rows
  - *value* check a single value, e.g. a *select count(\*)*. If a query result in more than one column, the evaluator will take into account only the first column in the first row

```python

   import nefertem as nt

   # Artifact Store
   STORE_LOCAL_01 = nt.StoreConfig(name="local",
                                   type="local",
                                   uri="./ntruns",
                                   isDefault=True)


   # Data Resource
   RES_LOCAL_01 = nt.DataResource(path="path-to-data",
                                  name="example_resource",
                                  store="local")


   # EXAMPLE CONSTRAINTS

   # Empty/non-empty table. The evaluation is allowed when check is "rows"

   # Expecting empty table as result of the validation query
   CONSTRAINT_01 = nt.ConstraintDuckDB(title="Example duckdb constraint",
                                       name="example-const",
                                       resources=["example_resource"],
                                       query="select * from example_resource",
                                       expect="empty",
                                       check="rows",
                                       weight=5)

   # Expecting non-empty table as result of the validation query
   CONSTRAINT_02 = nt.ConstraintDuckDB(title="Example duckdb constraint",
                                       name="example-const",
                                       resources=["example_resource"],
                                       query="select * from example_resource",
                                       expect="non-empty",
                                       check="rows",
                                       weight=5)

   # Exact value

   # Expecting a table with 10 rows
   CONSTRAINT_03 = nt.ConstraintDuckDB(title="Example duckdb constraint",
                                       name="example-const",
                                       resources=["example_resource"],
                                       query="select field from example_resource",
                                       expect="exact",
                                       check="rows",
                                       value=10,
                                       weight=5)

   # Expecting a table with 10 as result of the count
   CONSTRAINT_04 = nt.ConstraintDuckDB(title="Example duckdb constraint",
                                       name="example-const",
                                       resources=["example_resource"],
                                       query="select count(field) from example_resource",
                                       expect="exact",
                                       check="value",
                                       value=10,
                                       weight=5)

   # Minimum/maximum (both check are inclusive of the value)

   # Expecting a table with number of rows >= 10
   CONSTRAINT_05 = nt.ConstraintDuckDB(title="Example duckdb constraint",
                                       name="example-const",
                                       resources=["example_resource"],
                                       query="select field from example_resource",
                                       expect="minimum",
                                       check="rows",
                                       value=10,
                                       weight=5)

   # Expecting a table with result of count <= 10
   CONSTRAINT_06 = nt.ConstraintDuckDB(title="Example duckdb constraint",
                                       name="example-const",
                                       resources=["example_resource"],
                                       query="select count(field) from example_resource",
                                       expect="maximum",
                                       check="value",
                                       value=10,
                                       weight=5)

   # Range (value expect a string of parentheses and number)

   # Expecting a table with number of rows > 10 and <= 15
   CONSTRAINT_07 = nt.ConstraintDuckDB(title="Example duckdb constraint",
                                       name="example-const",
                                       resources=["example_resource"],
                                       query="select field from example_resource",
                                       expect="range",
                                       check="rows",
                                       value="(10,15]",
                                       weight=5)

   # Expecting a table with resulting value >= 10.87 and < 15.63
   CONSTRAINT_08 = nt.ConstraintDuckDB(title="Example duckdb constraint",
                                       name="example-const",
                                       resources=["example_resource"],
                                       query="select mean(field) from example_resource",
                                       expect="rows",
                                       check="value",
                                       value="[10.87,15.63)",
                                       weight=5)
```

#### SQLAlchemy
----------

The parameters to define a `ConstraintSqlAlchemy` are the following:

- *query*, an SQL query that will be executed on the database
- *expect*, expected tipology of result

  - *empty* (only for *check = rows*)
  - *non-empty* (only for *check = rows*)
  - *exact*
  - *range*
  - *minimum*
  - *maximum*

- *value*, value expected

  * Please note that when *expect* is equals to *range*, this parameter accepts a string formatted as follows

    - "(num1, num2)" upper exclusive, lower exclusive
    - "(num1, num2]" upper exclusive, lower inclusive
    - "[num1, num2)" upper inclusive, lower exclusive
    - "[num1, num2]" upper inclusive, lower inclusive

  - *minimum* and *maximum* are inclusive

- *check*, tipology of result to evaluate

  - *rows* check number of rows
  - *value* check a single value, e.g. a *select count(\*)*. If a query result in more than one column, the evaluator will take into account only the first column in the first row

```python

   import nefertem as nt

   # Artifact Store
   CONFIG_SQL_01 = {
       "connection_string": f"postgresql://user:password@host:port/database"
   }
   STORE_SQL_01 = nt.StoreConfig(name="postgres",
                                 type="sql",
                                 uri=f"sql://database",
                                 config=CONFIG_SQL_01)
   # Data Resource
   RES_SQL_01 = nt.DataResource(path=f"sql://schema.table",
                                name="example_resource",
                                store="postgres")

   # EXAMPLE CONSTRAINTS

   # The sqlalchemy constraints are basically the same as duckdb ones

   # Expecting empty table as result of the validation query
   CONSTRAINT_01 = nt.ConstraintDuckDB(title="Example sqlalchemy constraint",
                                       name="example-const",
                                       resources=["example_resource"],
                                       query="select * from example_resource",
                                       expect="empty",
                                       check="rows",
                                       weight=5)
```

#### Evidently

The parameters to define a `ConstraintEvidently` are the following:

- *resource*, name of the resource to validate.
- *reference_resource*, name of the resource to use as a reference dataset for comparison-based tests (e.g., drift detection).
- *tests*, list of test specifications to apply. Each test is defined with the test name (*type* parameter) and the dictionary of optional
  test parameters to consider (*values*).

Note that for the moment the execution plugins require the presence of a user-initialized `Data context`.

```python

   import nefertem as nt

   # Artifact Store
   STORE_LOCAL_01 = nt.StoreConfig(name="local",
                                   type="local",
                                   uri="./ntruns",
                                   isDefault=True)

   # Data Resource
   RES_LOCAL_01 = nt.DataResource(path="path-to-data",
                                  name="example_resource",
                                  store="local")

  # Data Resource
   RES_LOCAL_02 = nt.DataResource(path="path-to-ref-data",
                                  name="reference_resource",
                                  store="local")

   # EXAMPLE CONSTRAINTS

   # Expecting maximum column value to be between 10 and 50
   CONSTRAINT_01 = nt.ConstraintEvidently(title="Example Evidently constraint",
                                                  name="const-evidently-01",
                                                  resource="example_resource",
                                                  reference_resource="reference_resource",
                                                  tests=[EvidentlyElement(
                                                    type="evidently.test_preset.DataQualityTestPreset",
                                                    values={"columns": ["col1", "col2", "col3"]},
                                                  )],
                                                  weight=5)
```
