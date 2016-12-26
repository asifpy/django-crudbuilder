import os
from setuptools import setup
import crudbuilder

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-crudbuilder',
    version=crudbuilder.VERSION,
    packages=['crudbuilder'],
    include_package_data=True,
    license='BSD License',
    description='A simple Django CRUD builder',
    url='https://github.com/asifpy/django-crudbuilder',
    author='Asif Jamadar',
    author_email='saluasif@gmail.com',
    long_description=read('README.rst'),
    install_requires=[
        'django_tables2',
        'six>=1.10.0'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
    ]
)
