dodoo-tester
============

.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: LGPL-3
.. image:: https://badge.fury.io/py/dodoo-tester.svg
    :target: http://badge.fury.io/py/dodoo-tester

``dodoo-tester`` is a set of useful Odoo maintenance functions.
They are available as CLI scripts (based on click-odoo_), as well
as composable python functions.

.. contents::

Script
~~~~~~
.. code:: bash

  Usage: dodoo-tester [OPTIONS]

    Run Odoo tests through modern pytest instead of unittest.

  Options:
    --git-dir TEXT       Autodetect changed modules (through git).
    -i, --include TEXT   Force test run on those modules.
    -e, --exclude TEXT   Force excluding those modules from tests. Even if a
                         change has been detected.
    -t, --tags TEXT      Filter on those test tags.
    --logfile FILE       Specify the log file.
    -d, --database TEXT  Specify the database name. If present, this parameter
                         takes precedence over the database provided in the Odoo
                         configuration file.
    --log-level TEXT     Specify the logging level. Accepted values depend on
                         the Odoo version, and include debug, info, warn, error.
                         [default: info]
    -c, --config FILE    Specify the Odoo configuration file. Other ways to
                         provide it are with the ODOO_RC or OPENERP_SERVER
                         environment variables, or ~/.odoorc (Odoo >= 10) or
                         ~/.openerp_serverrc.
    --help               Show this message and exit.


Useful links
~~~~~~~~~~~~

- pypi page: https://pypi.org/project/dodoo-tester
- code repository: https://github.com//dodoo-tester
- report issues at: https://github.com//dodoo-tester/issues

.. _click-odoo: https://pypi.python.org/pypi/click-odoo

Credits
~~~~~~~

Contributors:

- David Arnold (XOE_)
- Moises Lopez (VAUXOO_)
- Jesus Zapata (JZGITHUB_)

.. _XOE: https://xoe.solutions
.. _VAUXOO: https://vauxoo.com
.. _JZGITHUB: https://github.com/JesusZapata

Maintainer
~~~~~~~~~~

.. image:: https://erp.xoe.solutions/logo.png
   :alt: XOE Corp. SAS
   :target: https://xoe.solutions

This project is maintained by XOE Corp. SAS.
