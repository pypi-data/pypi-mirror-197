# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shadybackend']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0', 'discord.py>=2.2.0,<3.0.0']

entry_points = \
{'console_scripts': ['shadybackend = shadybackend:main']}

setup_kwargs = {
    'name': 'shadybackend',
    'version': '0.1.0',
    'description': 'The defualt tool-chain for the SHADY Stack.',
    'long_description': "# SHADY Stack\n\nAs the name implies, this is a less than kosher web stack based of the SWAG\nstack. I developed it for my projects as I am in university and web hosting can\nbe expensive. The shady stack consists of the following:\n\n1. A **S**tatic site hosted (GitHub Pages, GitLab Pages, etc.) \n2. Simplistic pages that communicate to the backend via a already existing web-app's Web\n   **H**ooks (Slack, Discord, Gsuit, GitHub Actions, etc.).  \n3. An **A**plication Bridge program that can read the calls to the webhooks and\n   pass them to the next component. \n4. A Backend **D**eamon that acutely presses the requests from the webhooks and\n   updates a local copy of the site tree as needed.  \n5. An application that regularly s**Y**ncs the local tree\n   with the remote tree served as the static site in step 1.\n\n## Documentation\n\nFor more information, see the [official documentation](https://user-1103.github.io/shady-stack/).\n",
    'author': 'USER 1103',
    'author_email': '79700949+user-1103@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
