from setuptools import setup, find_packages

setup(
    name='Mogistics',
    version='0.1',
    author='Sarah',
    description='Setup de mon projet',
    packages=find_packages(),
    package_data={
        'config': ['*.yaml']
    },
    install_requires=[
        'numpy',
        'matplotlib',
    ],
)
