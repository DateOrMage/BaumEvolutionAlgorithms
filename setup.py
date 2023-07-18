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
        # package_dir={'': 'baumeva'},
        packages=find_packages(),
        description='Python library for perform evolutional algorithm',
    )
