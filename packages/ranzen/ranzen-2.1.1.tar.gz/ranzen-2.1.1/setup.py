# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ranzen',
 'ranzen.hydra',
 'ranzen.torch',
 'ranzen.torch.optimizers',
 'ranzen.torch.transforms']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=4.5.0']

extras_require = \
{'all': ['pandas>=1.5.0,<2.0.0',
         'wandb>=0.12,<0.14',
         'loguru>=0.6.0,<0.7.0',
         'torch>=1.12.1',
         'numpy>=1.23.2,<2.0.0',
         'hydra-core>=1.3.0,<2.0.0',
         'neoconfigen>=2.3.3'],
 'hydra': ['hydra-core>=1.3.0,<2.0.0', 'neoconfigen>=2.3.3'],
 'logging': ['loguru>=0.6.0,<0.7.0'],
 'torch': ['torch>=1.12.1', 'numpy>=1.23.2,<2.0.0'],
 'wandb': ['pandas>=1.5.0,<2.0.0', 'wandb>=0.12,<0.14']}

setup_kwargs = {
    'name': 'ranzen',
    'version': '2.1.1',
    'description': 'A toolkit facilitating machine-learning experimentation.',
    'long_description': '# ranzen 🎒\n\nA python toolkit facilitating machine-learning experimentation.\n\n[Documentation](https://wearepal.github.io/ranzen/)\n\n## Install\n\nRun\n```\npip install ranzen\n```\n\nor install directly from GitHub:\n```\npip install git+https://github.com/wearepal/ranzen.git@main\n```\n',
    'author': 'PAL',
    'author_email': 'info@predictive-analytics-lab.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/wearepal/ranzen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8.0,<3.12',
}


setup(**setup_kwargs)
