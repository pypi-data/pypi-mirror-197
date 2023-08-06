import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sshnuke",
    version="0.0.1",
    author="zazzzSec",
    author_email="ian@zazzz.io",
    description="sshnuke",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zazzzSec/sshnuke",
    project_urls={
        "Bug Tracker": "https://github.com/zazzzSec/sshnuke/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "sshnuke/src"},
    packages=setuptools.find_packages(where="sshnuke/src"),
    python_requires=">=3.6",
)