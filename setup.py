from __future__ import with_statement

from setuptools import setup


def get_version():
    return '0.0.1'


tests_require = [
    'pytest>=3.0.2', 'pytest-cov', 'pytest-lazy-fixture', 'mock', 'patch',
    'requests',
]

dev_require = tests_require


setup(
    name='coinapi',
    version=get_version(),
    description='coinapi',
    long_description='',
    author='Jeong YunWon',
    author_email='coinapi@youknowone.org',
    url='https://github.com/youknowone/coinapi',
    packages=(
        'coinapi',
    ),
    package_data={
        'coinapi': [],
    },
    install_requires=[
        'attrs',
        'requests',
    ],
    tests_require=tests_require,
    extras_require={
        'tests': tests_require,
        'dev': dev_require,
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)  # noqa
