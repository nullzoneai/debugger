from setuptools import setup

setup(
    name="debugger-tools",
    version="0.1.1",  # Bumped version
    py_modules=["debug_server"],  # Point to single module
    entry_points={
        "console_scripts": [
            "start-debug-server=debug_server:run_server"
        ]
    },
    install_requires=[],  # No dependencies
    python_requires=">=3.6",
)
