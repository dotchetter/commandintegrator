import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="commandintegrator",
    version="1.2.9",
    author="Simon Olofsson",
    author_email="dotchetter@protonmail.ch",
    description="A framework and API for developing chatbots and other command-driven applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/commandintegrator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)