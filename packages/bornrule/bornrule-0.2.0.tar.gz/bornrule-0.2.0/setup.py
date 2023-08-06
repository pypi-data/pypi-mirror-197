# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bornrule', 'bornrule.sql', 'bornrule.torch']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.5', 'pandas>=1.1.5', 'scikit-learn>=0.24.2', 'scipy>=1.5.4']

setup_kwargs = {
    'name': 'bornrule',
    'version': '0.2.0',
    'description': "Classification with Born's rule",
    'long_description': '<img src="https://upload.wikimedia.org/wikipedia/en/thumb/0/08/Logo_for_Conference_on_Neural_Information_Processing_Systems.svg/1200px-Logo_for_Conference_on_Neural_Information_Processing_Systems.svg.png" align="right" height="128"/>This package implements the classifier proposed in:\n\n> Emanuele Guidotti and Alfio Ferrara. Text Classification with Born’s Rule. *Advances in Neural Information Processing Systems*, 2022.\n\n<div align="center">\n  [<a href="https://openreview.net/pdf?id=sNcn-E3uPHA">Paper</a>] -\n  [<a href="https://nips.cc/media/PosterPDFs/NeurIPS%202022/8d7628dd7a710c8638dbd22d4421ee46.png">Poster</a>] - \n  [<a href="https://bornrule.eguidotti.com">Docs</a>]\n</div>\n\n## Usage\n\n### Scikit-Learn\n\n```py\nfrom bornrule import BornClassifier\n```\n\n- Use it as any other `sklearn` classifier\n- Supports both dense and sparse input and GPU-accelerated computing via `cupy`\n- Documentation available [here](https://bornrule.eguidotti.com/sklearn/)\n\n### PyTorch\n\n```py\nfrom bornrule.torch import Born\n```\n\n- Use it as any other `torch` layer\n- Supports real and complex-valued inputs. Outputs probabilities in the range [0, 1]\n- Documentation available [here](https://bornrule.eguidotti.com/pytorch/)\n\n### SQL\n\n```py\nfrom bornrule.sql import BornClassifierSQL\n```\n\n- Use it for in-database classification\n- Supports inputs represented as json `{feature: value, ...}`\n- Documentation available [here](https://bornrule.eguidotti.com/sql/)\n\n## Paper replication\n\nThe replication code is available at https://github.com/eguidotti/bornrule\n\n## Cite as\n\n```bibtex\n@inproceedings{guidotti2022text,\n  title={Text Classification with Born\'s Rule},\n  author={Emanuele Guidotti and Alfio Ferrara},\n  booktitle={Advances in Neural Information Processing Systems},\n  editor={Alice H. Oh and Alekh Agarwal and Danielle Belgrave and Kyunghyun Cho},\n  year={2022},\n  url={https://openreview.net/forum?id=sNcn-E3uPHA}\n}\n```\n',
    'author': 'Emanuele Guidotti',
    'author_email': 'emanuele.guidotti@unine.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/eguidotti/bornrule',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
