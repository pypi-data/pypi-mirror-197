from setuptools import setup
from pathlib import Path


setup(
    name='gink',
    version='0.20230313',
    description='a system for storing data structures in lmdb',
    url='https://github.com/x5e/gink',
    author='Darin McGill',
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',
        "Intended Audience :: Developers",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='gink lmdb crdt history versioned',
    packages=['gink'],
    python_requires=">=3.8, <4",
    install_requires=[
        "wsproto",
        "sortedcontainers",
        "lmdb",
        "protobuf<=3.20.3",
    ],
    extras_require={
        "test": ["nose2"],
        "lint": ["mypy"],
    },
    license_files=["LICENSE"],
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type='text/markdown'
)
