import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="elecmon",
    version="0.0.6",
    author="Ismael Raya",
    author_email="phornee@gmail.com",
    description="Electricity monitor library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Phornee/elecmon",
    packages=setuptools.find_packages(),
    package_data={
        '': ['*.yml', 'data/*.db'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Home Automation"
    ],
    install_requires=[
               'baseutils_phornee>=0.1.1',
    ],
    python_requires='>=3.6',
)
