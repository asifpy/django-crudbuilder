import os
from setuptools import setup
import crudbuilder

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-crudbuilder',
    version=crudbuilder.VERSION,
    packages=['crudbuilder'],
    include_package_data=True,
    license='BSD License',
    description='A simple Django CRUD builder',
    url='https://github.com/asifpy/django-crudbuilder/archive/master.tar.gz',
    author='Asif Jamadar',
    author_email='saluasif@gmail.com',
    install_requires=[
        'django_tables2>=1.0.4',
        'six>=1.10.0'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
    ]
)
