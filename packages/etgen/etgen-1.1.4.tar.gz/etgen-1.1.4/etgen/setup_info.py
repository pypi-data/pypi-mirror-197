# -*- coding: UTF-8 -*-
# Copyright 2013-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

# This module has no docstring because it is to be execfile'd
# from `setup.py`, `etgen/__init__.py` and possibly some external
# tools, too.

install_requires = ['six', 'future', 'lxml', 'django', 'rstgen']

SETUP_INFO = dict(
    name='etgen',
    version='1.1.4',
    install_requires=install_requires,
    description="Use ElementTree to generate html, rst and other markup",
    license_files=['COPYING'],
    test_suite='tests',
    author='Rumma & Ko Ltd',
    author_email='info@lino-framework.org',
    url="https://github.com/lino-framework/etgen",
    long_description="""\

Utilities for generating html, xml and rst content from an
`ElementTree
<https://docs.python.org/2/library/xml.etree.elementtree.html>`_.

Inspired by Frederik Lundh's `ElementTree Builder
<http://effbot.org/zone/element-builder.htm>`_.

The central project homepage is http://etgen.lino-framework.org

""",
    classifiers="""\
Programming Language :: Python
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Framework :: Sphinx :: Extension
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
License :: OSI Approved :: GNU Affero General Public License v3
Natural Language :: English
Operating System :: OS Independent""".splitlines())

SETUP_INFO.update(packages=[n for n in """
etgen
etgen.intervat
etgen.odf
etgen.sepa
""".splitlines() if n])

SETUP_INFO.update(package_data=dict(), include_package_data=True)


def add_package_data(package, *patterns):
    l = SETUP_INFO['package_data'].setdefault(package, [])
    l.extend(patterns)
    return l


add_package_data('etgen.sepa', 'XSD/*.xsd')

# print(20180216, SETUP_INFO['package_data'])
# raw_input()
