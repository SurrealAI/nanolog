import os
from setuptools import setup


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read().strip()


setup(
    name='nanolog',
    version='0.1',
    author='Jim Fan',
    url='http://github.com/SurrealAI/nanolog',
    description='python logging on steroids, lightweight and convenient',
    long_description=read('README.rst'),
    keywords=['logging',
              'utility'],
    license='GPLv3',
    packages=['nanolog'],
    entry_points={
        'console_scripts': [
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Programming Language :: Python :: 3"
    ],
    install_requires=[
        "prettyprinter",
    ],
    python_requires='>=3.0',
    include_package_data=True,
    zip_safe=False
)
