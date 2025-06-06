# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import os
from setuptools import setup

README = """
See the README on `GitHub
<https://github.com/uw-it-aca/django-saferecipient-email-backend>`_.
"""

version_path = 'saferecipient/VERSION'
VERSION = open(os.path.join(os.path.dirname(__file__), version_path)).read()
VERSION = VERSION.replace("\n", "")

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='Django-Safe-EmailBackend',
    version=VERSION,
    packages=['saferecipient'],
    author="UW-IT Student & Educational Technology Services",
    author_email="aca-it@uw.edu",
    include_package_data=True,
    install_requires=[
        'django>=3.2,<6',
    ],
    license='Apache License, Version 2.0',
    description='A Django email backend that sends all emails to a given address',
    long_description=README,
    url='https://github.com/uw-it-aca/django-saferecipient-email-backend',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
