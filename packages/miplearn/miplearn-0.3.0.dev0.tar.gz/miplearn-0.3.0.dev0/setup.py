#  MIPLearn: Extensible Framework for Learning-Enhanced Mixed-Integer Optimization
#  Copyright (C) 2020-2022, UChicago Argonne, LLC. All rights reserved.
#  Released under the modified BSD license. See COPYING.md for more details.

from setuptools import setup, find_namespace_packages

setup(
    name="miplearn",
    version="0.3.0.dev0",
    author="Alinson S. Xavier",
    author_email="axavier@anl.gov",
    description="Extensible Framework for Learning-Enhanced Mixed-Integer Optimization",
    url="https://github.com/ANL-CEEESA/MIPLearn/",
    packages=find_namespace_packages(),
    python_requires=">=3.7",
)
