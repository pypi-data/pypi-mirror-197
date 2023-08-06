=======
deepaas
=======

.. _deepaas_2.1.0:

2.1.0
=====

.. _deepaas_2.1.0_Deprecation Notes:

Deprecation Notes
-----------------

.. releasenotes/notes/deprecate-openwhisk-be449ddfb9fa554c.yaml @ b'f6d3ef068879c2b34c94e395a249a027c58a6ab4'

- OpenWhisk integration is marked as deprecated.


.. _deepaas_2.0.0:

2.0.0
=====

.. _deepaas_2.0.0_Prelude:

Prelude
-------

.. releasenotes/notes/remove-deprecated-get-args-166d8535f5b23c1e.yaml @ b'ef413b264f2215275dee263109c87a76f943e214'

Fallback loading of arguments (from V1 style) is now removed.


.. releasenotes/notes/remove-v1-api-93dbfcdc2f4beb1d.yaml @ b'd2e8f025ed4bb9bc878642d0b39d172fdaf0f83a'

This new release removes support for the V1 API (marked as deprecated in version 1.0.0).


.. _deepaas_2.0.0_Upgrade Notes:

Upgrade Notes
-------------

.. releasenotes/notes/remove-deprecated-get-args-166d8535f5b23c1e.yaml @ b'ef413b264f2215275dee263109c87a76f943e214'

- The old way of returning the arguments, to load the arguments using the old
  ``get_*_args`` functions is now removed. If you were still relying on them
  (check the logs) you must migrate to using the argument parser as soon as
  possible. 

.. releasenotes/notes/remove-v1-api-93dbfcdc2f4beb1d.yaml @ b'd2e8f025ed4bb9bc878642d0b39d172fdaf0f83a'

- V1 API is now removed, therefore all modules using the ``deepaas.model``
  entrypoint will stop working. The ``--enable-v1`` configuration option is
  now removed.


.. _deepaas_2.0.0_Other Notes:

Other Notes
-----------

.. releasenotes/notes/remove-v1-api-93dbfcdc2f4beb1d.yaml @ b'd2e8f025ed4bb9bc878642d0b39d172fdaf0f83a'

- V1 support is now removed.


.. _deepaas_1.3.0:

1.3.0
=====

.. _deepaas_1.3.0_New Features:

New Features
------------

.. releasenotes/notes/deepaas-cli-6e8a8689baab3277.yaml @ b'd67e1a286d1227476608ca4875b432f02535c9b6'

- Include ``deepaas-cli`` a new command line tool that provides the same
  functionality as the API through the commandline. This is useful for
  execution of batch tasks in a HPC/HTC or batch system cluster.


.. _deepaas_1.2.1:

1.2.1
=====

.. _deepaas_1.2.1_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/unify-train-predict-261e92c21d9f47d1.yaml @ b'55a9e6d3e0cb2011944945f1355ef78612bdc20d'

- Fix [#83](https://github.com/indigo-dc/DEEPaaS/issues/87) out out memory
  errors due to the usage of two different executor pools.


.. _deepaas_1.2.0:

1.2.0
=====

.. _deepaas_1.2.0_New Features:

New Features
------------

.. releasenotes/notes/add-new-cli-669061dfada81f5c.yaml @ b'f6f6d30ded54e1731ef92780f394ca18ca6a3403'

- Include a new command line tool to execute inference and prediction calls 
  from the shell, whitout spawning a server and making cURL requests to it.
  This is useful for execution of batch tasks in a HPC/HTC or batch system
  cluster.


.. _deepaas_1.2.0_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/bug-fixes-73cfa32ffb5bdbb0.yaml @ b'f6f6d30ded54e1731ef92780f394ca18ca6a3403'

- This new release fixes an error introduced by `webargs` in its 6.0.0
  version.  Since we cannot yet fix it (`aiohttp-webargs` needs to be updated
  as well) we pin webargs to the 5.X.X versions
  https://github.com/indigo-dc/DEEPaaS/issues/82

.. releasenotes/notes/bug-fixes-73cfa32ffb5bdbb0.yaml @ b'f6f6d30ded54e1731ef92780f394ca18ca6a3403'

- Set `debug` in OpenWhisk mode as configured by the user.

