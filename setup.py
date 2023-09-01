from setuptools import setup, find_packages
import baumeva
import json
import os


def read_pipenv_dependencies(fname):
    """Получаем из Pipfile.lock зависимости по умолчанию."""
    filepath = os.path.join(os.path.dirname(__file__), fname)
    with open(filepath) as lockfile:
        lockjson = json.load(lockfile)
        return [dependency for dependency in lockjson.get('default')]


if __name__ == '__main__':
    setup(
        name='baumeva',
        version=baumeva.__version__,
        packages=find_packages(),
        description='Python library for perform evolution algorithm',
        license='MIT',
        author='Aleksei Kudryavtsev',
        author_email='vatutu@gmail.com',
        url='https://github.com/DateOrMage/BaumEvolutionAlgorithms',
        keywords=['genetic', 'algorithm', 'optimization', 'crossover', 'population', 'selection', 'mutation', 'fitness',
                  'evolutionary', 'adaptive', 'chromosome', 'genome', 'binary'],
        classifiers=["Programming Language :: Python :: 3",
                     "Programming Language :: Python :: 3.7",
                     "Programming Language :: Python :: 3.8",
                     "Programming Language :: Python :: 3.9",
                     "Programming Language :: Python :: 3.10",
                     "Programming Language :: Python :: 3.11",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent"]
    )
