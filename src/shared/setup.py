from setuptools import setup, find_packages

setup(
    name="shared",
    version="0.0.1",
    packages=find_packages(),
    py_modules=[
        "config",
        "errors",
    ],
    install_requires=[
        "setuptools~=75.8.0",
        "fastapi~=0.115.5",
        "pydantic~=2.10.0",
        "pydantic-settings~=2.6.1",
        "SQLAlchemy~=2.0.36",
        "asyncpg~=0.30.0",
    ],
)
