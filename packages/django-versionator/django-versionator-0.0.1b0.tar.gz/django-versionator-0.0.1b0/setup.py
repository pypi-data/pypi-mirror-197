import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-versionator",
    version="0.0.1b",
    author="AlexCLeduc",
    # author_email="author@example.com",
    # description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlexCleduc/django-versionator",
    packages=[
        # find_packages() also includes extraneous stuff, like testing and django_sample
        package
        for package in setuptools.find_packages()
        if package.startswith("versionator")
    ],
    install_requires=[],
    tests_require=["django"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
