Configurations
==============

* `Stores`_
* `Data Resource`_
* `Run configuration`_
* `Constraints`_

Stores
------

nefertem.StoreConfig
^^^^^^^^^^^^^^^^^^^^^

.. autopydantic_model:: nefertem.utils.config::StoreConfig

Data Resource
-------------

nefertem.DataResource
^^^^^^^^^^^^^^^^^^^^^^

.. autopydantic_model:: nefertem.utils.config::DataResource

Run configuration
-----------------

nefertem.RunConfig
^^^^^^^^^^^^^^^^^^^

.. autopydantic_model:: nefertem.utils.config::ExecConfig

.. autopydantic_model:: nefertem.utils.config::RunConfig

Constraints
-----------

Every constraint inherit from the base Contraint model.

nefertem.Constraint
^^^^^^^^^^^^^^^^^^^^
.. autopydantic_model:: nefertem.utils.config::Constraint

nefertem.ConstraintFrictionless
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autopydantic_model:: nefertem.utils.config::ConstraintFrictionless

nefertem.ConstraintFullFrictionless
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autopydantic_model:: nefertem.utils.config::ConstraintFullFrictionless


nefertem.ConstraintDuckDB
^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autopydantic_model:: nefertem.utils.config::ConstraintDuckDB

nefertem.ConstraintSqlAlchemy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autopydantic_model:: nefertem.utils.config::ConstraintSqlAlchemy

nefertem.ConstraintGreatExpectations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autopydantic_model:: nefertem.utils.config::ConstraintGreatExpectations

