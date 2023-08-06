import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="apiflows",
    version="1.0.5",
    author="Allen",
    author_email="aiddroid@gmail.com",
    description="A yaml data-drive HTTP API testing tools.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aiddroid/apiflows",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)