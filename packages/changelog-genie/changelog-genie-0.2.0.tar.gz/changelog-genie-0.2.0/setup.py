# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['changelog_genie']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['changelog_genie = changelog_genie.cli:cli']}

setup_kwargs = {
    'name': 'changelog-genie',
    'version': '0.2.0',
    'description': 'Generate changelogs for GitHub projects efficiently',
    'long_description': '# Changelog Genie\n\n![](changelog-genie.png)\n\nImage Credit: DALL-E\n\n## Overview\n\nChangelog Genie is a simple and pragmatic changelog generator, implemented in Python, that utilizes the GitHub \nREST API to produce changelog content very efficiently, avoiding GitHub API rate limits. It was built out of necessity \nas a replacement for [github-changelog-generator](https://github.com/github-changelog-generator/github-changelog-generator),\nwhich served well for many Apache Arrow projects for a long time but eventually became unworkable as the number of \nissues and pull requests continued to grow.\n\nRoadmap/Status:\n\n- [x] Basic functionality in place\n- [ ] Make sections and labels configurable\n- [ ] Support reading [github-changelog-generator](https://github.com/github-changelog-generator/github-changelog-generator) configuration files\n- [ ] Write the content into an existing changelog file\n\n## Installation\n\n```pip3 install changelog-genie```\n\n## Usage\n\n```text\n$ changelog_genie --help\nusage: cli.py [-h] project tag1 tag2\n\npositional arguments:\n  project     The project name e.g. apache/arrow-datafusion\n  tag1        The previous release tag\n  tag2        The current release tag\n\noptions:\n  -h, --help  show this help message and exit\n\n```\n\nThere is currently a two-step process for generating a changelog. This will be improved in a future release.\n\n### Step 1: Generate Partial Changelog \n\nRun the ChangeLog Genie script to fetch the commits between two tags from GitHub and produce the changelog \ncontent. Providing a GitHub token is necessary to achieve a higher rate limit for interaction with the GitHub REST API. \n\n```shell\nGITHUB_TOKEN=<token> changelog_genie andygrove/changelog-genie 0.1.0 0.2.0 > changelog-0.2.0.md\n```\n\n### Step 2: Copy and paste into existing changelog\n\nThis will be automated in a future release.\n\n## Contributing\n\n```shell\npython3 -m venv venv\n# activate the venv\nsource venv/bin/activate\n# update pip itself if necessary\npython -m pip install -U pip\n# install dependencies (for Python 3.8+)\npython -m pip install -r requirements.in\n\nPoetry\n\n```shell\nsudo apt install python3-poetry\n```\n\nTesting\n\n```shell\npoetry build\npoetry install\n```\n\n',
    'author': 'Andy Grove',
    'author_email': 'andygrove73@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
