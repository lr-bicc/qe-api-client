import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyqlikengine",
    version="0.0.4",
    author="Rumen Vasilev",
    author_email="R.Vasilev@LRWorld.com",
    description="Python wrapper around Qlik Engine JSON API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lr-bicc/pyqlikengine",
    package_dir={'pyqlikengine': 'pyqlikengine'},
    packages=setuptools.find_packages(exclude=["test"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'websocket-client>=0.47.0'
    ],
    python_requires='>=3.6',
)
