import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "gremlin-rest",
    version = "0.0.1",
    author = "Roman Suvorov",
    author_email = "windj007@gmail.com",
    description = ("Simple Gremlin REST client"),
    license = "BSD",
    keywords = "rest client Gremlin Blueprints TinkerPop",
    url = "http://packages.python.org/gremlin-rest",
    packages=['gremlin_rest', 'gremlin_rest.tests'],
    package_data={'gremlin_rest': ['scripts/*.groovy']},
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
    ],
    requires = ['gremlin_rest', 'gremlin_rest.tests', 'gremlinpy', 'pyarc'],
    test_suite = "gremlin_rest.tests.all_tests",
)