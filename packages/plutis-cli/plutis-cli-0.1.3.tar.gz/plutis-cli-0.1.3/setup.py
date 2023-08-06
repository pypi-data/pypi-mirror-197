from setuptools import setup, find_packages

setup(
    name="plutis-cli",
    version="0.1.3",
    packages=find_packages(),
    install_requires=["PyYAML", "requests"],
    entry_points={
        "console_scripts": [
            "plutis=plutis_cli.main:main",
        ]
    },
)