import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "BiasBuster",
    version = "0.0.4",
    author = "Nathalie Rzepka",
    # author_email = "author@example.com",
    description = "A Python package to check for algorithmic bias.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/nathalierze/BiasBuster",
    project_urls = {
        "Bug Tracker": "https://github.com/nathalierze/BiasBuster/issuesL",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.6"
)