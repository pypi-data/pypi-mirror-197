# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pitertools']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pitertools',
    'version': '0.3.0',
    'description': '',
    'long_description': '# pitertools\nTools to process python iterators in parallel.\n\n## map_parallel\nSpin up n threads to pull from input iterator and run an operation on it in parallel\n\n## Roadmap\n- Add automated testing, publishing\n- Add more tests \n- Add some linter, static type checking\n- Allow running on external executor\n- Add asyncio implementation\n',
    'author': 'tsah',
    'author_email': 'tsah.weiss@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tsah/pitertools',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8.0,<3.9.0',
}


setup(**setup_kwargs)
