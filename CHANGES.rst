Changes
~~~~~~~

Future (?)
----------
- who knows...

0.6.6 (2019-06-02)
------------------
- Inbclude camptocamp pytest tool for BDD

0.6.5 (2019-05-05)
------------------
- Simplify repo structure
- Fix package namespace issues

0.6.0 (2019-01-24)
------------------
- Refactor to dodoo plugin

0.5.4 (2018-12-05)
------------------
- Add addons-path option

0.5.3 (2018-12-04)
--------------------
- Improve 0.5.2 fix: generically use bytes for py3 and str for py2 envs

0.5.2 (2018-12-04)
--------------------
- Origin refspec fix: during fetching the origin, the refspec was read and
  temporarliy stored. This is because we need to override narrowed CI induced
  refspecs in some cases. However, it was read with a newline caracter, which
  then was written back corrupting the git repository.

0.5.1 (2018-12-04)
--------------------
- First PyPI release
- Module change detection fixes
- Testing db teardown (close leaked db conections)

0.5.0 (2018-11-04)
--------------------
- Start of project
