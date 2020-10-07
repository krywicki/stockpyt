import setuptools

setuptools.setup(
    name="stockpyt",
    version="0.0.1dev",
    install_requires=[
        "requests~=2.24"
    ],
    extra_requires={
        "dotenv":["python-dotenv"]
    }
)