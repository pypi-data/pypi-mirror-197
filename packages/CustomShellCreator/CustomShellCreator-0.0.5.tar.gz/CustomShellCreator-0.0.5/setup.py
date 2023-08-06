import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CustomShellCreator",
    version="0.0.5",
    author="Chinmay Malvania",
    author_email="chinmay.malvania@gmail.com",
    description="A package to create custom shells",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chinmaym505/CustomShellCreator",
    project_urls={
        "Bug Tracker": "https://github.com/chinmaym505/CustomShellCreator/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3",
)
