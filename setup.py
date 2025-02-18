from setuptools import setup, find_packages
setup(
    name="secret_santa_assigner",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=2.0.0"
    ],
    entry_points={
        "console_scripts": [
            "secret-santa=secret_santa_assigner.__main__:main"
        ]
    },
)