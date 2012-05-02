from setuptools import setup
import os

readme = os.path.join(os.path.dirname(__file__), 'README.rst')

setup(
    name='marchanddesable',
    version='0.1',
    url='https://github.com/madjar/marchanddesable',
    license='ISC',
    author='Georges Dubus',
    author_email='georges.dubus@compiletoi.net',
    description='Turn off your server when you sleep',
    long_description=open(readme).read(),
    classifiers=[
        'License :: OSI Approved :: ISC License (ISCL)',
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        ],
    py_modules=['marchanddesable'],
    entry_points={
        'console_scripts': [ 'marchand = marchanddesable:main' ],
        },

    tests_require = ['nose', 'mock'],
    test_suite = "nose.collector",
)
