from setuptools import setup, find_packages

VERSION = '13.2.0'
DESCRIPTION = 'nazca4sdk'
LONG_DESCRIPTION = 'SDK pythonowe'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="nazca4sdk",
    version=VERSION,
    author="M_APA",
    author_email="martyna.kurbiel@apagroup.pl",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["setuptools",
                      "numpy",
                      "pandas",
                      "mysql-connector-python",
                      "pip",
                      "configparser",
                      "wheel",
                      "py",
                      "Sphinx",
                      "tzlocal",
                      "six",
                      "requests",
                      "pydantic",
                      "clickhouse_driver",
                      "urllib3",
                      "kafka-python",
                      "datetime",
                      "typing",
                      "dask~=2022.12.1",
                      "clickhouse-connect"],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'nazca4sdk'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
