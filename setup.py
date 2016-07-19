#!/usr/bin/env python
from setuptools import setup, find_packages


dev_requires = [
    'Sphinx==1.2.2'
]

tests_require = [
    'factory_boy==2.4.1',
    'mock==1.0.1',
    'mock-django==0.6.6',
    'six>=1.7.3',
    'sqlalchemy>=1.0.12',
]

install_requires = [
    'nodeconductor>=0.102.2',
    'python-gitlab>=0.9',
]

setup(
    name='nodeconductor-gitlab',
    version='0.1.0.dev0',
    author='OpenNode Team',
    author_email='info@opennodecloud.com',
    url='http://nodeconductor.com',
    description='GitLab service provides an interface to GitLab repository manager.',
    long_description=open('README.rst').read(),
    package_dir={'': 'src'},
    packages=find_packages('src', exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']),
    install_requires=install_requires,
    zip_safe=False,
    extras_require={
        'test': tests_require,
        'dev': dev_requires,
    },
    entry_points={
        'nodeconductor_extensions': (
            'nodeconductor_gitlab = nodeconductor_gitlab.extension:GitLabExtension',
        ),
    },
    tests_require=tests_require,
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
    ],
)
