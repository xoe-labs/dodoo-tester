# Copyright 2018 ACSONE SA/NV (<http://acsone.eu>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name="dodoo-tester",
    description="dodoo tester script",
    long_description="\n".join(
        (
            open(os.path.join(here, "README.rst")).read(),
            open(os.path.join(here, "CHANGES.rst")).read(),
        )
    ),
    use_scm_version=True,
    packages=find_packages(),
    setup_requires=["setuptools-scm"],
    install_requires=[
        "dodoo>=2.0.0.rc6",
        "future",
        "pytest",
        "pyyaml==3.12 ; python_version < '3.7'",
        "pyyaml==3.13 ; python_version >= '3.7'",
    ],
    license="LGPLv3+",
    author="XOE Labs",
    author_email="info@xoe.solutions",
    url="http://github.com/xoe-labs/dodoo-tester",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: "
        "GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Framework :: Odoo",
    ],
    entry_points="""
        [core_package.cli_plugins]
        test=dodoo_tester.cli:test
        pytest=dodoo_tester.cli:pytest
    """,
)
