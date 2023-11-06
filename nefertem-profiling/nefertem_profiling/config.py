PLUGINS = {
    "frictionless": ["nefertem_profiling.plugins.frictionless.builder", "ProfilingBuilderFrictionless"],
    "ydata_profiling": ["nefertem_profiling.plugins.ydata_profiling.builder", "ProfilingBuilderYdataProfiling"],
    "evidently": ["nefertem_profiling.plugins.evidently.builder", "ProfilingBuilderEvidently"],
    "_dummy": ["nefertem_profiling.plugins._dummy.builder", "ProfilingBuilderDummy"],
}
