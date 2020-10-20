import setuptools

setuptools.setup(
    name="stockpyt",
    version="0.0.1",
    python_requires = ">=3.8",
    install_requires=[
        "requests~=2.24",
        "rich~=8.0"
    ],
    entry_points={
        "console_scripts": [
            "stockpyt=stockpyt.cli:main",
        ],
    },
    extras_require={
        "dev":["python-dotenv"]
    }
)
