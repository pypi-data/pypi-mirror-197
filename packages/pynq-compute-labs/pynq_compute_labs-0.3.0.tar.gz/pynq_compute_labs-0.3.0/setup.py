#  Copyright (C) 2020 Xilinx, Inc
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from setuptools import setup, find_packages
from pynqutils.setup_utils import build_py, extend_package

__author__ = "Peter Ogden"
__copyright__ = "Copyright 2020, Xilinx"
__email__ = "pynq_support@xilinx.com"

data_files = []
module_name = "pynq_compute_labs"

with open("README.md", encoding="utf-8") as fh:
    readme_lines = fh.readlines()[2:]
long_description = ("".join(readme_lines))

extend_package(module_name, data_files)

setup(name=module_name,
      version="0.3.0",
      description="Package for the PYNQ Compute Acceleration Labs",
      long_description=long_description,
      long_description_content_type="text/markdown",
      author="Peter Ogden",
      author_email="pynq_support@xilinx.com",
      packages=find_packages(),
      package_data={
          "": data_files,
      },
      python_requires=">=3.8.0",
      # keeping 'setup_requires' only for readability - relying on
      # pyproject.toml and PEP 517/518
      setup_requires=[
          "pynq>=3.0.1",
          "pynqutils>=0.1.1"
      ],
      install_requires=[
          "pynq>=3.0.1",
          "pynqutils>=0.1.1",
          "IPython",
          "lz4"
      ],
      entry_points={
          "pynq.notebooks": [
               "0-introduction = pynq_compute_labs.notebooks.introduction",
               "pynq_compute = pynq_compute_labs.notebooks.labs"
          ]
      },
      cmdclass={"build_py": build_py},
      license="Apache License 2.0"
      )
