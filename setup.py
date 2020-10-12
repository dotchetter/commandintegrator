import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="commandintegrator",
    version="13",
    author="Simon Olofsson",
    author_email="dotchetter@protonmail.ch",
    description="A framework and API for developing chatbots and other command-driven applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dotchetter/commandintegrator",
    packages=[
        "commandintegrator",
        "commandintegrator.baseclasses",
        "commandintegrator.core",
        "commandintegrator.models",
        "commandintegrator.tools"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pytz",
        "requests",
        "urllib3"
    ],
    data_files=[
        ('config', [
            "commandintegrator\\language.json",
            "commandintegrator\\commandintegrator.settings"
            ]
        )
    ],
    python_requires='>=3.8',
    include_package_data=True
)