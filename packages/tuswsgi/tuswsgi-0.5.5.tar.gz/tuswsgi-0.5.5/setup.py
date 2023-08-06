import os

from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    long_description = f.read()


setup(
    name='tuswsgi',
    version='0.5.5',
    description='python wsgi filter for tus protocol 1.0.0',
    long_description=long_description,
    url='https://github.com/mvdbeek/tusfilter',
    author='Marius van den Beek',
    author_email='m.vandenbeek@gmail.com',
    keywords='tus wsgi filter',
    license='MIT',

    py_modules=['tuswsgi'],
    install_requires=['WebOb'],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
        'License :: OSI Approved :: MIT License',
    ],
)
