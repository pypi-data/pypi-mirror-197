# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyleague',
 'pyleague.domain',
 'pyleague.entrypoint',
 'pyleague.infrastructure',
 'pyleague.tests',
 'pyleague.use_cases']

package_data = \
{'': ['*'], 'pyleague': ['files/*']}

install_requires = \
['typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['pyleague = pyleague.entrypoint.main:app']}

setup_kwargs = {
    'name': 'pyleague',
    'version': '0.2.0',
    'description': "Pyleague is a cli tool that helps organizing competitions. After providing pyleague with a list of the competition's participants you will be able to get the matches for each day of the competition.",
    'long_description': '# Pyleague\n\n## Index\n\n1. [Overview](#overview)\n2. [Requirements](#requirements)\n3. [Installation](#installation)\n4. [Configuration](#configuration)\n5. [Tests](#tests)\n6. [Deployment](#deployment)\n   7.[Getting started:](#getting_started)\n\n## <a name="overview">Overview</a>\n\nPyleague is a cli tool that helps organizing competitions.\nAfter providing pyleague with a list of the competition\'s participants\nyou will be able to get the matches for each day of the competition.\n\n## <a name="requirements">Requirements</a>\n\n* System requirements\n\npython >= 3.9\n\n* Package requirements\n\nListed in pyproject.toml under \'[tool.poetry.dependencies]\'\n\n## <a name="installation">Installation</a>\n\n### For use\n\nFetch it from pip\n\n```bash\npip install pyleague\n```\n\n### For development\n\nTo install package dependencies, install [poetry](https://python-poetry.org/docs/), then run the following command:\n\n```bash\npoetry install\n```\n\n## <a name="tests">Tests</a>\n\nFrom root directory run:\n\n~~~\npytest pyleague/tests\n~~~\n\n## <a name="deployment">Deployment</a>\n\nUse poetry\n\n```commandline\npoetry build\n```\n\n```commandline\npoetry publish\n```\n\n## <a name="getting_started">Getting started</a>\n\nTo try the app:\n\n* Install it\n\n* On your terminal run\n\n```commandline\npyleague init\n```\n\nDefine your league participants as asked.\n\n* Check the matches for today\n\n```commandline\npyleague today\n```\n\n* Update the league to the next day\n\n```commandline\npyleague next\n```\n\n```commandline\npyleague today\n```\n',
    'author': 'mf-andres',
    'author_email': 'amunoz@gradiant.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mf-andres/pyleague',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
