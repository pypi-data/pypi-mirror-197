import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="open_pyxl_sql",
    version="0.12.0",
    author="Fabien BATTINI",
    author_email="fabien.battini@gmail.com",
    description="A tiny SQL engine for Excel files, based on Openpyxl",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/fabien.battini/pyxlsql",
    packages=setuptools.find_packages(),
    classifiers=[
        # see https://pypi.org/classifiers/
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business :: Office Suites",
    ],
    python_requires='>=3.6',
)

