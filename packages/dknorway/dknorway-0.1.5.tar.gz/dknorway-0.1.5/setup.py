#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""dknorway - Models to hold Fylke, Kommune and PostSted + import script of file from Bring (Posten).
"""

classifiers = """\
Development Status :: 3 - Alpha
Intended Audience :: Developers
Programming Language :: Python
Programming Language :: Python :: 3
Topic :: Software Development :: Libraries
"""

import setuptools

version = '0.1.5'


setuptools.setup(
    name='dknorway',
    version=version,
    url="https://github.com/datakortet/dknorway",
    maintainer="Bjorn Pettersen",
    maintainer_email="bp@datakortet.no",
    requires=[],
    install_requires=[
        'Django',
        'requests',
        "django-extensions==2.1.0",
    ],
    description=__doc__.strip(),
    classifiers=[line for line in classifiers.split('\n') if line],
    long_description=open('README.rst').read(),
    packages=setuptools.find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
)
