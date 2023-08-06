# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['TensorState', 'TensorState.models']

package_data = \
{'': ['*']}

install_requires = \
['numcodecs>=0.11.0,<0.12.0', 'numpy>=1.24.2,<2.0.0', 'zarr>=2.14.2,<3.0.0']

setup_kwargs = {
    'name': 'tensorstate',
    'version': '0.4.0',
    'description': '',
    'long_description': "# TensorState (v0.4.0) - Neural Network Efficiency Tools\n\nTensorState is a toolbox to capture neural network information to better\nunderstand how information flows through the network. The core of the toolbox is\nthe ability to capture and analyze neural layer state space, which logs unique\nfiring states of neural network layers. This repository implements and extends\nthe work by Schaub and Hotaling in their paper,\n[Assessing Intelligence in Artificial Neural Networks](https://arxiv.org/abs/2006.02909).\n\n## Installation\n\nPrecompiled wheels exist for Windows, Linux, and MacOS for Python 3.6-3.8. No\nspecial installation instructions are required in most cases:\n\n`pip install pip --upgrade`\n\n`pip install TensorState`\n\nIf the wheels don't download or you run into an error, try installing the\npre-requisites for compiling before installing with `pip`.\n\n`pip install pip --upgrade`\n\n`pip install numpy==1.19.2 Cython==3.0a1`\n\n`pip install TensorState`\n\n## Documentation\n\nhttps://tensorstate.readthedocs.io/en/latest/\n",
    'author': 'Nicholas-Schaub',
    'author_email': 'nicholas.j.schaub@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
