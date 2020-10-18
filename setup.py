import setuptools

setuptools.setup(
    name="stockpyt",
    version="0.0.1dev",
    install_requires=[
        "requests~=2.24",
        "rich~=8.0"
    ],
    extras_require={
        "dev":["python-dotenv"]
    }
)
