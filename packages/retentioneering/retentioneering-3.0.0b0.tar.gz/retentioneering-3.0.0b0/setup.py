# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['retentioneering',
 'retentioneering.backend',
 'retentioneering.backend.callback',
 'retentioneering.constants',
 'retentioneering.data_processor',
 'retentioneering.data_processors_lib',
 'retentioneering.datasets',
 'retentioneering.datasets.data',
 'retentioneering.edgelist',
 'retentioneering.eventstream',
 'retentioneering.eventstream.helpers',
 'retentioneering.exceptions',
 'retentioneering.graph',
 'retentioneering.nodelist',
 'retentioneering.params_model',
 'retentioneering.preprocessor',
 'retentioneering.templates',
 'retentioneering.templates.p_graph',
 'retentioneering.templates.transition_graph',
 'retentioneering.tooling',
 'retentioneering.tooling.clusters',
 'retentioneering.tooling.cohorts',
 'retentioneering.tooling.constants',
 'retentioneering.tooling.describe',
 'retentioneering.tooling.describe_events',
 'retentioneering.tooling.event_timestamp_hist',
 'retentioneering.tooling.funnel',
 'retentioneering.tooling.mixins',
 'retentioneering.tooling.stattests',
 'retentioneering.tooling.step_matrix',
 'retentioneering.tooling.step_sankey',
 'retentioneering.tooling.timedelta_hist',
 'retentioneering.tooling.transition_matrix',
 'retentioneering.tooling.typing',
 'retentioneering.tooling.typing.transition_graph',
 'retentioneering.tooling.user_lifetime_hist',
 'retentioneering.transition_graph',
 'retentioneering.utils',
 'retentioneering.widget']

package_data = \
{'': ['*']}

install_requires = \
['jupyterlab>=3.4.7,<4.0.0',
 'networkx>=2.8.6,<3.0.0',
 'notebook>=6.4.12,<7.0.0',
 'numpy>=1.21.5,<1.24',
 'pandas-stubs>=1.4.4,<2.0.0',
 'pandas>=1.5.0,<2.0.0',
 'plotly>=5.10.0,<6.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'scipy>=1.3,<1.9',
 'seaborn>=0.12.1,<0.13.0',
 'statsmodels>=0.13.5,<0.14.0',
 'umap-learn>=0.5.3,<0.6.0',
 'virtualenv>=20.17']

setup_kwargs = {
    'name': 'retentioneering',
    'version': '3.0.0b0',
    'description': 'Product analytics and marketing optimization framework based on deep user trajectories analysis',
    'long_description': 'None',
    'author': 'Retentioneering User Trajectory Analysis Lab',
    'author_email': 'retentioneering@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/retentioneering/retentioneering-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
