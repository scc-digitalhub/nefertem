
Profiling
=========

The profiling is the process where a framework try to profile a `DataResource`
optionally in accordance to a given `Metric` model specification. If
`Metric` model is not specified, the profiling evaluates built-in set of properties
and metrics.


Run methods
-----------

```python

   import nefertem as nt

   # Creating run ...

   with run:

       run.profile()
       run.profile_wrapper()
       run.profile_nefertem()
       run.log_profile()
       run.persist_profile()

Execution methods
^^^^^^^^^^^^^^^^^

Execution method tells plugings to execute profiling over a resource. All this methods accept specific framework arguments as argument and optionally a list of `Metric` models to evaluate.

* `run.profile()`, execute both framework profiling and nefertem profile parsing
* `run.profile_wrapper()`, execute only framework profiling, return a specific framework artifact
* `run.profile_nefertem()`, execute both framework profiling and nefertem profile parsing, return a `NefertemProfile`. `NefertemProfile` object contains *metrics* list with results of the the evaluated metrics and *field_metrics* dictionary containing the list of metric results for each field (if applicable).

Data and metadata persistence
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* `run.log_profile()`, log `NefertemProfile` into the `MetadataStore`
* `run.profile()`, persist artifact into the default `ArtifactStore`

Supported libraries
-------------------

* `Frictionless`_
* `Pandas Profiling`_
* `Great Expectation`_
* `Evidently` _

Frictionless
------------

```python

   run_config = {

       # The only parameter accepted is "frictionless"
       "library": "frictionless",

       # execArgs accepted are the ones passed to the constructor of Resource().
       "execArgs": {}

   }


Pandas Profiling
----------------

```python

   run_config = {

       # The only parameter accepted is "pandas_profiling"
       "library": "pandas_profiling",

       # execArgs accepted are the ones passed to the method ProfileReport(). E.g.:
       "execArgs": {"minimal": True}

   }


Great Expectation
-----------------

The `great_expectations` profiler executes a profiling operation on a specified `DataResource`
using validator profling model.

```python

   run_config = {
       "library": "great_expectations",

       # There are no suitable execution arguments for the great_expectations validator
       "execArgs": {}

   }

Evidently
^^^^^^^^^^^^^^^^^^

The `evidently` profiler executes a report evaluation given a specified *metric* model on a `DataResource`.

```python

   run_config = {
       "library": "evidently",

       # There are no suitable execution arguments for the evidently validator
       "execArgs": {}

   }
