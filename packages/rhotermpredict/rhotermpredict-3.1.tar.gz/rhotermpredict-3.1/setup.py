from setuptools import setup, find_packages
setup(
    name="rhotermpredict",
    version="3.1",
    packages=["rhotermpredict"],
    package_dir={'rhotermpredict': 'rhotermpredict'},

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=['numpy >= 1.15.4', 'Bio >= 0.1.0'],

    # metadata to display on PyPI
    author="Cameron Roots",
    author_email="croots@utexas.edu",
    description="Barrick Lab fork of Salvo 2019 RhoTermPredict",
    keywords="",
    url="https://github.com/barricklab/RhoTermPredict",   # project home page, if any
    project_urls={
        "Bug Tracker": "https://github.com/barricklab/RhoTermPredict/issues",
        "Source Code": "https://github.com/barricklab/RhoTermPredict",
    },
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3"
    ],
    entry_points={
        'console_scripts' : [
          'rhotermpredict = rhotermpredict.algorithm:main',
        ],
    },

    # could also include long_description, download_url, etc.
)
