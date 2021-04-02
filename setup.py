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
    author="UW-IT AXDD",
    author_email="aca-it@uw.edu",
    include_package_data=True,
    install_requires=[
        'Django>=2.1,<3.2',
    ],
    license='Apache License, Version 2.0',
    description='A django email backend that sends all emails to a given address',
    long_description=README,
    url='https://github.com/uw-it-aca/django-saferecipient-email-backend',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],
)
