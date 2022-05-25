from setuptools import setup, find_packages

setup(
    name='funlang',
    packages=find_packages(include=('funlang',)),
    install_requires=['anytree'],
    entry_points={
        'console_scripts': [
            'funlang = funlang.cli:entrypoint'
        ]
    }
)
