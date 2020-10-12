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
    packages=[
        'commandintegrator.baseclasses',
        'commandintegrator.core',
        'commandintegrator.models',
        'commandintegrator.tools'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "aiohttp >= 3.6.2",
        "async-timeout >= 3.0.1",
        "attrs >= 19.3.0",
        "certifi >= 2020.4.5.1",
        "chardet >= 3.0.4",
        "idna >= 2.9",
        "multidict >= 4.7.5",
        "pytz >= 2019.3",
        "requests >= 2.23.0",
        "style >= 1.1.0",
        "update >= 0.0.1",
        "urllib3 >= 1.25.8",
        "websockets >= 8.1",
        "yarl >= 1.4.2"
    ],
    python_requires='>=3.8',
)