PLUGINS = {
    "frictionless": ["nefertem_validation.plugins.frictionless.builder", "ValidationBuilderFrictionless"],
    "evidently": ["nefertem_validation.plugins.evidently.builder", "ValidationBuilderEvidently"],
    "duckdb": ["nefertem_validation.plugins.duckdb.builder", "ValidationBuilderDuckDB"],
    "sqlalchemy": ["nefertem_validation.plugins.sqlalchemy.builder", "ValidationBuilderSqlAlchemy"],
    "_dummy": ["nefertem_validation.plugins._dummy.builder", "ValidationBuilderDummy"],
}
