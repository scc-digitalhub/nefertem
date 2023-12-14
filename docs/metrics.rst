
Metrics
===========

A ``Metric`` is a container for the profile evaluation rules to be reported on the resource.
You can define as many ``Metric`` as you want, and *nefertem* will pass them to the desired framework of profiling.
By default, some frameworks have built in metrics to be evaluated and the specification is not required.
When the frameworks requires explicit evaluation input, this model allows for specifying that.

``Metrics`` share the following parameters

* *name*, identifier for the metric
* *title*, optional, human readable version of the identifier
* *resources*, targeted LIST of resources

Metric types
----------------

* `Evidently`_

Evidently
------------------

The parameters to define a ``MetricEvidently`` are the following:

* *resource*, name of the resource to validate.
* *reference_resource*, name of the resource to use as a reference dataset for comparison-based reports (e.g., drift detection).
* *metrics*, list of metric specifications to apply. Each test is defined with the report name (*type* parameter) and the dictionary of optional
  metric parameters to consider (*values*).

Note that for the moment the execution plugins require the presence of a user-initialized ``Data context``.

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

   # EXAMPLE METRICS

   # Expecting maximum column value to be between 10 and 50
   METRIC_01 = nt.MetricEvidently(title="Example Evidently metric",
                                                  name="metric-evidently-01",
                                                  resource="example_resource",
                                                  reference_resource="reference_resource",
                                                  tests=[EvidentlyElement(
                                                    type="evidently.metric_preset.DataQualityPreset",
                                                    values={"columns": ["col1", "col2", "col3"]},
                                                  )])
