from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="animo_trainer",
    version="0.1.4",
    description="Animo Trainer",
    long_description=long_description,
    license_files = ('LICENSE.txt',),
    license="Copyright (c) 2023 Transitional Forms Inc. All Rights Reserved.",
    author="Transitional Forms",
    author_email="dante@transforms.ai",
    url="https://transforms.ai/",
    packages=['animo_trainer'],
    include_package_data=True,
    python_requires=">=3.9,<3.10",
    entry_points={
        "console_scripts": [
            "animo-learn=animo_trainer.main:main",
        ],
    },
    install_requires = [
        "protobuf==3.20",
        "mlagents==0.30.0",
        "pythonnet==3.0.1",
        "torch==1.11.0",
    ]
)
