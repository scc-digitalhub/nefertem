"""
PluginBuilder registry.
"""
# Dummy imports
from nefertem.plugins.inference.dummy_inference import InferenceBuilderDummy
from nefertem.plugins.profiling.dummy_profiling import ProfileBuilderDummy
from nefertem.plugins.validation.dummy_validation import ValidationBuilderDummy
from nefertem.utils.commons import (
    LIBRARY_DUMMY,
    OPERATION_INFERENCE,
    OPERATION_PROFILING,
    OPERATION_VALIDATION,
)

# Registry of plugin builders

REGISTRY = {
    OPERATION_INFERENCE: {
        LIBRARY_DUMMY: InferenceBuilderDummy,
    },
    OPERATION_PROFILING: {
        LIBRARY_DUMMY: ProfileBuilderDummy,
    },
    OPERATION_VALIDATION: {
        LIBRARY_DUMMY: ValidationBuilderDummy,
    },
}


# frictionless imports
try:
    from nefertem.plugins.inference.frictionless_inference import (
        InferenceBuilderFrictionless,
    )
    from nefertem.plugins.profiling.frictionless_profiling import (
        ProfileBuilderFrictionless,
    )
    from nefertem.plugins.validation.frictionless_validation import (
        ValidationBuilderFrictionless,
    )
    from nefertem.utils.commons import LIBRARY_FRICTIONLESS

    REGISTRY[OPERATION_INFERENCE][LIBRARY_FRICTIONLESS] = InferenceBuilderFrictionless
    REGISTRY[OPERATION_PROFILING][LIBRARY_FRICTIONLESS] = ProfileBuilderFrictionless
    REGISTRY[OPERATION_VALIDATION][LIBRARY_FRICTIONLESS] = ValidationBuilderFrictionless

except ImportError:
    ...

# great_expectations imports
try:
    from nefertem.plugins.profiling.great_expectations_profiling import (
        ProfileBuilderGreatExpectations,
    )
    from nefertem.plugins.validation.great_expectations_validation import (
        ValidationBuilderGreatExpectations,
    )
    from nefertem.utils.commons import LIBRARY_GREAT_EXPECTATIONS

    REGISTRY[OPERATION_PROFILING][
        LIBRARY_GREAT_EXPECTATIONS
    ] = ProfileBuilderGreatExpectations
    REGISTRY[OPERATION_VALIDATION][
        LIBRARY_GREAT_EXPECTATIONS
    ] = ValidationBuilderGreatExpectations

except ImportError:
    ...

# pandas_profiling imports
try:
    from nefertem.plugins.profiling.pandas_profiling_profiling import (
        ProfileBuilderPandasProfiling,
    )
    from nefertem.utils.commons import LIBRARY_PANDAS_PROFILING

    REGISTRY[OPERATION_PROFILING][
        LIBRARY_PANDAS_PROFILING
    ] = ProfileBuilderPandasProfiling

except ImportError:
    ...

# ydata_profiling imports
try:
    from nefertem.plugins.profiling.ydata_profiling_profiling import (
        ProfileBuilderYdataProfiling,
    )
    from nefertem.utils.commons import LIBRARY_YDATA_PROFILING

    REGISTRY[OPERATION_PROFILING][
        LIBRARY_YDATA_PROFILING
    ] = ProfileBuilderYdataProfiling

except ImportError:
    ...

# duckdb imports
try:
    from nefertem.plugins.validation.duckdb_validation import ValidationBuilderDuckDB
    from nefertem.utils.commons import LIBRARY_DUCKDB

    REGISTRY[OPERATION_VALIDATION][LIBRARY_DUCKDB] = ValidationBuilderDuckDB

except ImportError:
    ...

# sqlalchemy imports
try:
    from nefertem.plugins.validation.sqlalchemy_validation import (
        ValidationBuilderSqlAlchemy,
    )
    from nefertem.utils.commons import LIBRARY_SQLALCHEMY

    REGISTRY[OPERATION_VALIDATION][LIBRARY_SQLALCHEMY] = ValidationBuilderSqlAlchemy

except ImportError:
    ...

try:
    from nefertem.plugins.validation.evidently_validation import (
        ValidationBuilderEvidently,
    )
    from nefertem.utils.commons import LIBRARY_EVIDENTLY

    REGISTRY[OPERATION_VALIDATION][LIBRARY_EVIDENTLY] = ValidationBuilderEvidently

except ImportError:
    ...
