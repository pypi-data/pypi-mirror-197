import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tessng2other",
    version="0.0.1",
    author="Author",
    author_email="17315487709@163.com",
    description="convert tessng to file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    python_requires='>=3.6, <=3.9',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
