# debugger/setup.py
from setuptools import setup, find_packages

setup(
    name="debugger-tools",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "start-debug-server=debugger.server:main"
        ]
    },
    install_requires=[],
    description="Debugging utilities for sandbox environments",
    long_description="Helper tools for debugging and monitoring applications",
)
