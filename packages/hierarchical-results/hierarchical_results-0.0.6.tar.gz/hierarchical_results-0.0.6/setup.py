#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

requirements = ["numpy", "pandas", "pathos", "shared_memory_wrapper"]

test_requirements = ['pytest>=3', "hypothesis"]

setup(
    author="Ivar Grytten",
    author_email='ivargry@ifi.uio.no',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Hierarchical results",
    entry_points={
        'console_scripts': [
            'hierarchical_results=hierarchical_results.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description="Hierarchical results",
    include_package_data=True,
    keywords='hierarchical_results',
    name='hierarchical_results',
    packages=find_packages(include=['hierarchical_results', 'hierarchical_results.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/ivargr/hierarchical_results',
    version='0.0.6',
    zip_safe=False,
)
