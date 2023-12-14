# Modules

`nefertem` is an extensible framework that allows to add new functionalities through the use of plugins.

There are two types of plugins:

- **operations**, plugins that allow to execute operations of data quality
- **plugins**, plugins that allow to extend the functionalities of the operations through the use of new frameworks

The **operations** extend the functionalities of the `run` object, and includes new methods to execute and new metadata to log. They also define the a specific **plugin** category related to them. These **plugins** are the ones that actually execute the operations.

Out-of-the-box, `nefertem` provides the following operations:

- `inference`
- `profiling`
- `validation`
- `metrics`

## Inference

The inference is the process where a framework try to infer the data schema of a `DataResource`.

### Run methods

```python
with run:
    run.infer()
    run.log_schema()
    run.persist_schema()
```

### Execution methods

Execution method tell plugings to execute inference over a resource. All this methods accept specific framework arguments as argument.

- `run.infer()`, execute both framework inference and nefertem schema parsing
- `run.infer_wrapper()`, execute only framework inference, return a specific framework artifact
- `run.infer_nefertem()`, execute both framework inference and nefertem schema parsing, return a `NefertemSchema`

### Data and metadata persistence

- `run.log_schema()`, log `NefertemSchema` locally
- `run.persist_schema()`, persist artifact locally

### Supported libraries

- `Frictionless`

#### Frictionless

```python
run_config = {
    "library": "frictionless",
    # execArgs accepted are the ones passed to the method Schema.describe().
    # Note that arguments `path` and `name` are already taken.
    "execArgs": {}
}
```

## Profiling

The profiling is the process where a framework try to profile a `DataResource`
optionally in accordance to a given `Metric` model specification. If
`Metric` model is not specified, the profiling evaluates built-in set of properties
and metrics.

### Run methods

```python
with run:
    run.profile()
    run.log_profile()
    run.persist_profile()
```

### Execution methods

Execution method tells plugings to execute profiling over a resource. All this methods accept specific framework arguments as argument and optionally a list of `Metric` models to evaluate.

- `run.profile()`, execute both framework profiling and nefertem profile parsing
- `run.profile_wrapper()`, execute only framework profiling, return a specific framework artifact
- `run.profile_nefertem()`, execute both framework profiling and nefertem profile parsing, return a `NefertemProfile`.

### Data and metadata persistence

- `run.log_profile()`, log `NefertemProfile` locally
- `run.persist_profile()`, persist artifact locally

### Supported libraries

- `Frictionless`
- `Ydata_Profiling`

#### Frictionless

```python
run_config = {
    "library": "frictionless",
    # execArgs accepted are the ones passed to the constructor of Resource().
    "execArgs": {}
}
```

### Ydata_Profiling

```python
run_config = {
    "library": "ydata_profiling",
    # execArgs accepted are the ones passed to the method ProfileReport(). E.g.:
    "execArgs": {"minimal": True}
}
```

#### Evidently

The `evidently` profiler executes a report evaluation given a specified *metric* model on a `DataResource`.

```python
run_config = {
    "library": "evidently",
    # There are no suitable execution arguments for the evidently validator
    "execArgs": {}

}
```

## Validation

The validation is the process where a framework validate one or more `DataResource` in accordance to a given `Constraint`.

### Run methods

```python
with run:
    run.validate()
    run.log_report()
    run.persist_report()
```

### Execution methods

Execution method tells plugings to execute validation over a resource. All this methods accept specific framework arguments as argument and a list of `Constraint` to validate.

- `run.validate()`, execute both framework validation and nefertem report parsing
- `run.validate_wrapper()`, execute only framework validation, return a specific framework artifact
- `run.validate_nefertem()`, execute both framework validation and nefertem report parsing, return a `NefertemReport`

### Data and metadata persistence

- `run.log_report()`, log `NefertemReport` locally
- `run.persist_report()`, persist artifact locally

### Supported libraries

- `Frictionless`
- `DuckDB`
- `SQLAlchemy`
- `Evidently`

#### Frictionless

```python
run_config = {
    "library": "frictionless",
    # execArgs accepted are the ones passed to the method validate()
    "execArgs": {}
}
```

#### DuckDB

```python
run_config = {
    "library": "duckdb",
    # There are no suitable execution arguments for the duckdb validator
    "execArgs": {}
}
```

#### SQLAlchemy

The `sqlalchemy` validator executes query defined in a *constraints* on the database side. To execute a validation without execution errors, there MUST be at least one user defined `SQLArtifactStore` passed to a `Client` and a `DataResource` associated with that store.

```python
run_config = {
    "library": "sqlalchemy",
    # There are no suitable execution arguments for the duckdb validator
    "execArgs": {}
}
```

#### Evidently

The `evidently` validator executes a test suite specified in a *constraint* on a `DataResource`.

```python
run_config = {
    "library": "evidently",
    # There are no suitable execution arguments for the evidently validator
    "execArgs": {}
}
```

### Constraints

A `Constraint` is a rule that resource must fit to be considered valid.
You can define as many `Constraint` as you want, and `nefertem` will pass them to the desired framework of validation.

`Constraints` share the following parameters

- *name*, identifier for the constraint
- *type*, type of the constraint
- *title*, optional, human readable version of the identifier
- *resources*, targeted LIST of resources
- *weight*, optional, importance of an eventual error

### Constraint types

- `Frictionless`
- `Frictionless schema`
- `DuckDB`
- `SQLAlchemy`
- `Evidently`

#### Frictionless

The parameters to define a `ConstraintFrictionless` are the following:

- *field*, specified targeted field
- *field_type*, specified targeted field type
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
# Input store configuration
store_local_01 = {"name": "local", "type": "local"}

# Data Resource
res_local_01 = {
    "path": "path-to-data",
    "name": "example-resource",
    "store": "local"
}

# Example constraint. We expect that the values of the
# specified field have a maximum length of 11 characters.
constraint_01 = {
    "type": "frictionless",
    "title": "Example frictionless constraint",
    "name": "example-const",
    "resources": ["example-resource"],
    "field": "field-to-validate",
    "field_type": "string",
    "constraint": "maxLength",
    "value": 11,
}
```

#### Frictionless schema

The parameters to define a `ConstraintFullFrictionless` are the following:

- *schema*, a dictionary (or a frictionless `Schema`), formatted as `frictionless Schema`.

Example:

```python
# Input store configuration
store_local_01 = {"name": "local", "type": "local"}

# Data Resource
res_local_01 = {
    "path": "path-to-data",
    "name": "example-resource",
    "store": "local"
}

schema_01 = {
    "fields": [
        {"name":"col1", "type": "string"},
        {"name":"col2", "type": "integer"},
        {"name":"col3", "type": "float"},
    ]
}

# Example constraint. We will pass to a validator a full frictionless schema.
constraint_01 = {
    "type": "frictionless_full",
    "title": "Example frictionless_schema constraint",
    "name": "example-const",
    "resources": ["example-resource"],
    "table_schema": schema_01,
}
```

#### DuckDB

The parameters to define a `ConstraintDuckDB` are the following:

- *query*, an SQL query that will be executed on the resources. Note that the query require some precautions

    1. When you select from a resource, the resource must be written lowercase
    2. The name of the resource where you select from must be in the list of resources passed to the constraint

- *expect*, expected tipology of result

  - *empty* (only for *check = rows*)
  - *non-empty* (only for *check = rows*)
  - *exact*
  - *range*
  - *minimum*
  - *maximum*

- *value*, value expected (note that when *expect* is equals to *range*, this parameter accepts a string formatted as follows)

    1. "(num1, num2)" upper exclusive, lower exclusive
    2. "(num1, num2]" upper exclusive, lower inclusive
    3. "[num1, num2)" upper inclusive, lower exclusive
    4. "[num1, num2]" upper inclusive, lower inclusive

  - *minimum* and *maximum* are inclusive

- *check*, tipology of result to evaluate

  - *rows* check number of rows
  - *value* check a single value, e.g. a *select count(\*)*. If a query result in more than one column, the evaluator will take into account only the first column in the first row

```python
# Input store configuration
store_local_01 = {"name": "local", "type": "local"}

# Data Resource
res_local_01 = {
    "path": "path-to-data",
    "name": "example-resource",
    "store": "local"
}

# Empty/non-empty table. The evaluation is allowed when check is "rows"

# Expecting empty table as result of the validation query
constraint_01 = {
    "type": "duckdb",
    "name": "example-const",
    "resources": ["example_resource"],
    "query": "select * from example_resource",
    "expect": "empty",
    "check": "rows",
}

# Expecting non-empty table as result of the validation query
constraint_02 = {
    "type": "duckdb",
    "name": "example-const",
    "resources": ["example_resource"],
    "query": "select * from example_resource",
    "expect": "non-empty",
    "check": "rows",
}

# Exact value

# Expecting a table with 10 rows
constraint_03 = {
    "type": "duckdb",
    "name": "example-const",
    "resources": ["example_resource"],
    "query": "select field from example_resource",
    "expect": "exact",
    "check": "rows",
    "value": 10,
}

# Expecting a table with 10 as result of the count
constraint_04 = {
    "type": "duckdb",
    "name": "example-const",
    "resources": ["example_resource"],
    "query": "select count(field) from example_resource",
    "expect": "exact",
    "check": "value",
    "value": 10,
}

# Minimum/maximum (both check are inclusive of the value)

# Expecting a table with number of rows >= 10
constraint_05 = {
    "type": "duckdb",
    "name": "example-const",
    "resources": ["example_resource"],
    "query": "select field from example_resource",
    "expect": "minimum",
    "check": "rows",
    "value": 10,
}

# Expecting a table with result of count <= 10
constraint_06 = {
    "type": "duckdb",
    "name": "example-const",
    "resources": ["example_resource"],
    "query": "select count(field) from example_resource",
    "expect": "maximum",
    "check": "value",
    "value": 10,
}

# Range (value expect a string of parentheses and number)

# Expecting a table with number of rows > 10 and <= 15
constraint_07 = {
    "type": "duckdb",
    "name": "example-const",
    "resources": ["example_resource"],
    "query": "select field from example_resource",
    "expect": "range",
    "check": "rows",
    "value": "(10,15]",
}

# Expecting a table with resulting value >= 10.87 and < 15.63
constraint_08 = {
    "type": "duckdb",
    "name": "example-const",
    "resources": ["example_resource"],
    "query": "select mean(field) from example_resource",
    "expect": "rows",
    "check": "value",
    "value": "[10.87,15.63)",
}
```

#### SQLAlchemy

The parameters to define a `ConstraintSqlAlchemy` are the following:

- *query*, an SQL query that will be executed on the database
- *expect*, expected tipology of result

  - *empty* (only for *check = rows*)
  - *non-empty* (only for *check = rows*)
  - *exact*
  - *range*
  - *minimum*
  - *maximum*

- *value*, value expected (note that when *expect* is equals to *range*, this parameter accepts a string formatted as follows)

    1. "(num1, num2)" upper exclusive, lower exclusive
    2. "(num1, num2]" upper exclusive, lower inclusive
    3. "[num1, num2)" upper inclusive, lower exclusive
    4. "[num1, num2]" upper inclusive, lower inclusive

  - *minimum* and *maximum* are inclusive

- *check*, tipology of result to evaluate

  - *rows* check number of rows
  - *value* check a single value, e.g. a *select count(\*)*. If a query result in more than one column, the evaluator will take into account only the first column in the first row

```python
# Input store configuration
config_sql_01 = {
    "driver": "postgresql+psycopg2",
    "host": "host",
    "port": "port",
    "user": "user",
    "password": "password",
    "database": "database"
}
store_sql_01 = {
    "name": "postgres",
    "type": "sql",
    "config": config_sql_01
}

# Data Resource
res_sql_01 = {
    "path": f"sql://database/table",
    "name": "example_resource",
    "store": "postgres"
}

# EXAMPLE CONSTRAINTS

# The sqlalchemy constraints are basically the same as duckdb ones

# Expecting empty table as result of the validation query
constraint_01 = {
    "type": "sqlalchemy",
    "name": "example-const",
    "resources": ["example_resource"],
    "query": "select * from example_resource",
    "expect": "empty",
    "check": "rows",
}
```

#### Evidently

The parameters to define a `ConstraintEvidently` are the following:

- *resource*, name of the resource to validate.
- *reference_resource*, name of the resource to use as a reference dataset for comparison-based tests (e.g., drift detection).
- *tests*, list of test specifications to apply. Each test is defined with the test name (*type* parameter) and the dictionary of optional
  test parameters to consider (*values*).

Note that for the moment the execution plugins require the presence of a user-initialized `Data context`.

```python
# Input store configuration
store_local_01 = {"name": "local", "type": "local"}

# Data Resource
res_local_01 = {
    "path": "path-to-data",
    "name": "example-resource",
    "store": "local"
}

# Data Resource reference
res_local_02 = {
    "path": "path-to-ref-data",
    "name": "reference-resource",
    "store": "local"
}

# EXAMPLE CONSTRAINTS

# Expecting maximum column value to be between 10 and 50
constraint_01 = {
    "type": "evidently",
    "name": "const-evidently-01",
    "resource": "example_resource",
    "reference_resource": "reference_resource",
    "tests": [{
            "type": "evidently.test_preset.DataQualityTestPreset",
            "values": {"columns": ["col1", "col2", "col3"]},
        }]
}
```

## Metrics

TODO
