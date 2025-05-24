import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qe-api-client",
    version="2.8.0",
    author="Rumen Vasilev",
    author_email="R.Vasilev@LRWorld.com",
    description="Python client for the Qlik Engine JSON API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lr-bicc/qe-api-client",
    package_dir={'qe_api_client': 'qe_api_client'},
    packages=setuptools.find_packages(exclude=["test", "examples", "docs"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'websocket-client>=1.0.0',
        'pandas>=2.2.0',
        'numpy>=2.0.0',
        'uuid>=1.0'
    ],
    python_requires='>=3.6',
)
