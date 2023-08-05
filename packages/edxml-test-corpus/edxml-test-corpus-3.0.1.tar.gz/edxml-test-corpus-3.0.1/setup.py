import os
import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


tests = package_files('edxml_test_corpus/tests')

setuptools.setup(
    name="edxml-test-corpus",
    version="3.0.1",
    author="Dik Takken",
    author_email="dik.takken@edxml.org",
    description="A collection of portable unit tests for EDXML implementations",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/edxml/test-corpus",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Testing",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
    package_data={
        '': tests
    },
)
