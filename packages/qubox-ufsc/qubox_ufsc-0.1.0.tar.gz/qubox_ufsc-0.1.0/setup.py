# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['qubox_ufsc']

package_data = \
{'': ['*']}

install_requires = \
['ket-lang>=0.5.0.1,<0.6.0.0', 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'qubox-ufsc',
    'version': '0.1.0',
    'description': 'Client for the QuBOX UFSC',
    'long_description': '# QuBOX UFSC Client\n\nQuBOX is a portable quantum computing simulator developed by Quantuloop\nfor the [Ket language](https://quantumket.org). Accelerated by GPU, QuBOX has two simulation modes, \nbeing able to simulate more than 30 quantum bits.\n    \nIn partnership with Quantuloop, the Quantum Computing Group - UFSC provides\nfree remote access to a QuBOX simulator. You can use this client to access \nthe QuBOX hosted at the Federal University of Santa Catarina (UFSC).\n\nSee <https://qubox.ufsc.br> for more information.\n\n## Installation\n\n```shell\npip install qubox-ufsc\n```\n\n## Usage\n\n```python\nfrom ket import * # import quantum types and functions\nimport qubox_ufsc # import the QuBOX UFSC Client\n\n\n# Request access to the QuBOX UFSC\nqubox_ufsc.login(\n    name="Your Name",\n    email="you_email@example.com",\n    affiliation="Your Affiliation"\n)\n\n# Configure the quantum execution\nqubox_ufsc.config(\n    mode="sparse",\n    precision=1,\n) # Every quantum execution after this line will run on the QuBOX\n\n##################################\n# Bell State preparation example #\n##################################\na, b = quant(2)\ncnot(H(a), b)\nprint(dump(a+b).show())\n```\n',
    'author': 'Quantuloop',
    'author_email': 'contact@quantuloop.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<4',
}


setup(**setup_kwargs)
