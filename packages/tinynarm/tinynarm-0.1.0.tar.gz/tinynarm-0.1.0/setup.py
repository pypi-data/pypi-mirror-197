# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tinynarm']

package_data = \
{'': ['*']}

install_requires = \
['niaarm>=0.3.1,<0.4.0']

setup_kwargs = {
    'name': 'tinynarm',
    'version': '0.1.0',
    'description': 'Simplify numerical association rule mining',
    'long_description': '# tinyNARM\n\n## About\n\ntinyNARM is an experimental effort in approaching/tailoring the classical Numerical Association Rule Mining (NARM) to limited hardware devices, e.g., ESP32 microcontrollers so that devices do not need to depend on remote servers for making decisions. Motivation mainly lies in smart agriculture, where Internet connectivity is unavailable in rural areas.\n\nThe current repository hosts a tinyNARM algorithm prototype initially developed in Python for fast prototyping.\n\n## Detailed insights\nThe current version includes (but is not limited to) the following functions:\n\n- loading datasets in CSV format,\n- discretizing numerical features to discrete classes,\n- association rule mining using the tinynarm approach,\n- easy comparison with the NiaARM approach.\n\n## Installation\n\n### pip\n\nInstall tinyNARM with pip:\n\n```sh\npip install tinynarm\n```\n\n## Usage\n\n### Basic run\n\n```python\nfrom tinynarm import TinyNarm\nfrom tinynarm.utils import Utils\n\ntinynarm = TinyNarm("new_dataset.csv")\ntinynarm.create_rules()\n\npostprocess = Utils(tinynarm.rules)\npostprocess.rules_to_csv("rules.csv")\npostprocess.generate_statistics()\n```\n\n### Discretization\n\n```python\nfrom tinynarm.discretization import Discretization\n\ndataset = Discretization("datasets/sportydatagen.csv", 5)\ndata = dataset.generate_dataset()\ndataset.dataset_to_csv(data, "new_dataset.csv")\n```\n\n## NARM references\n\n[1] I. Fister Jr., A. Iglesias, A. Gálvez, J. Del Ser, E. Osaba, I Fister. [Differential evolution for association rule mining using categorical and numerical attributes](http://www.iztok-jr-fister.eu/static/publications/231.pdf) In: Intelligent data engineering and automated learning - IDEAL 2018, pp. 79-88, 2018.\n\n[2] I. Fister Jr., V. Podgorelec, I. Fister. [Improved Nature-Inspired Algorithms for Numeric Association Rule Mining](https://link.springer.com/chapter/10.1007/978-3-030-68154-8_19). In: Vasant P., Zelinka I., Weber GW. (eds) Intelligent Computing and Optimization. ICO 2020. Advances in Intelligent Systems and Computing, vol 1324. Springer, Cham.\n\n[3] I. Fister Jr., I. Fister [A brief overview of swarm intelligence-based algorithms for numerical association rule mining](https://arxiv.org/abs/2010.15524). arXiv preprint arXiv:2010.15524 (2020).\n\n[4] Stupan, Ž., Fister, I. Jr. (2022). [NiaARM: A minimalistic framework for Numerical Association Rule Mining](https://joss.theoj.org/papers/10.21105/joss.04448.pdf). Journal of Open Source Software, 7(77), 4448.\n\n## License\n\nThis package is distributed under the MIT License. This license can be found online at <http://www.opensource.org/licenses/MIT>.\n\n## Disclaimer\n\nThis framework is provided as-is, and there are no guarantees that it fits your purposes or that it is bug-free. Use it at your own risk!\n',
    'author': 'Iztok Fister Jr.',
    'author_email': 'iztok@iztok-jr-fister.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/firefly-cpp/tinynarm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
