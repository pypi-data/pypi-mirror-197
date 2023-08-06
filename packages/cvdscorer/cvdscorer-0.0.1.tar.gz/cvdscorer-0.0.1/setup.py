from setuptools import setup

with open("README.md", 'r') as fh:
    long_description = fh.read()

setup(
    name='cvdscorer',
    version='0.0.1',
    description='Tool to calculate cardio-vascular disease risk',
    py_modules=['helloworld'],
    package_dir={'': 'src', },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "pandas >=1",
    ],
    extras_require={
        "dev": ["pytest >=3.7", ],
    },
    url="https://github.com/PeterPirog/CVDScorer",
    author="Peter Pirog",
    author_email="peterpirogtf@gmail.com"
)
