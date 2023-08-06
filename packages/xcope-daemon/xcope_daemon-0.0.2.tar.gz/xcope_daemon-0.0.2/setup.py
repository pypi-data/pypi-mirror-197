import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xcope_daemon",
    packages=['xcope_daemon'],
    package_dir={'': 'src'},
    version="0.0.2",
    author="rwecho",
    author_email="rwecho@live.com",
    description="Xcope diagnose daemon sdk. ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "grpcio==1.51.1",
        "protobuf==4.22.1",
    ],
    python_requires='>=3.6',
)
