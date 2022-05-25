from setuptools import setup, find_packages

setup(
    name='funlang',
    packages=find_packages(include=('funlang',)),
    entry_points={
        'console_scripts': [
            'funlang = funlang.cli:entrypoint'
        ]
    }
)
