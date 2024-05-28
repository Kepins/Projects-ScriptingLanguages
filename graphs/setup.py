from setuptools import setup, Extension

module = Extension(
    'simple_graphs',
    sources=['simple_graphs.c'],
)

setup(
    name='simple_graphs',
    version='1.0',
    description='simple_graphs C Extension',
    ext_modules=[module],
)
