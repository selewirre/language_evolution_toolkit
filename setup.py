import setuptools

__author__ = "Selewirre Iskvary"
__license__ = "GNU GPL v3 license"
__description__ = "A tool for evolving languages."
__email__ = "selewirre@gmail.com"
__version__ = "0.0.5"

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="language_evolution_toolkit",
    version=__version__,
    author=__author__,
    author_email=__email__,
    description=__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/selewirre/language_evolution_toolkit",
    packages=setuptools.find_packages(),
    package_dir={'language_evolution_toolkit': 'language_evolution_toolkit'},
    package_data={'language_evolution_toolkit': []},
    install_requires=[
        'ipapy'
        'multipledispatch',
        'numpy'
    ],
    license=__license__,
    classifiers=[
        "Programming Language :: Python :: 3",
        f"License :: {__license__}",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
