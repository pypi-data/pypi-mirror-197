import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "product_apriori",
    version = "0.0.1",
    author = "DIY",
    author_email = "joyce.chan@mrdiy.com",
    packages=['product_apriori'],
    description = "Apriori product relation test",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "package URL",
    project_urls = {
        "Bug Tracker": "package issues URL",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "product_apriori"},
    packages = setuptools.find_packages(where="product_apriori"),
    python_requires = ">=3.6"
)