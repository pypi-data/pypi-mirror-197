# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['psdm_analysis',
 'psdm_analysis.analysis',
 'psdm_analysis.io',
 'psdm_analysis.models',
 'psdm_analysis.models.input',
 'psdm_analysis.models.input.connector',
 'psdm_analysis.models.input.container',
 'psdm_analysis.models.input.participant',
 'psdm_analysis.models.result',
 'psdm_analysis.models.result.grid',
 'psdm_analysis.models.result.participant',
 'psdm_analysis.plots',
 'psdm_analysis.plots.results',
 'psdm_analysis.processing']

package_data = \
{'': ['*']}

install_requires = \
['jupyter>=1.0.0,<2.0.0',
 'matplotlib>=3.6.0,<4.0.0',
 'numpy>=1.24.1,<2.0.0',
 'pandas>=1.4.1,<2.0.0',
 'plotly>=5.6.0,<6.0.0',
 'requests>=2.27.1,<3.0.0',
 'scipy>=1.10.0,<2.0.0',
 'seaborn>=0.12.1,<0.13.0']

setup_kwargs = {
    'name': 'psdm-analysis',
    'version': '0.1.2.dev3',
    'description': '',
    'long_description': '# psdm-analysis\n\nThe psdm-analysis tool is meant to parse the [Power System Data Model (PSDM)](https://github.com/ie3-institute/PowerSystemDataModel) as well as provide calculation and plotting utilities to analyze the respective data.\n\nIt is currently under development and therefore highly unstable. So if you want to use it, expect it to change quite frequently for now.',
    'author': 'Thomas Oberliessen',
    'author_email': 'thomas.oberliessen@googlemail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.8.1,<3.12',
}


setup(**setup_kwargs)
