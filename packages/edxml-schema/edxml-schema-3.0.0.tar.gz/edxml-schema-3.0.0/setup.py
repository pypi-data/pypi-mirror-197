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


schema = package_files('edxml_schema/schema')

setuptools.setup(
    name="edxml-schema",
    version="3.0.0",
    author="Dik Takken",
    author_email="dik.takken@edxml.org",
    description="The RelaxNG schema that is part of the EDXML specification",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/edxml/schema",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
    package_data={
        '': schema
    },
)
