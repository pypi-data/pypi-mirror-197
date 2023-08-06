# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['youtrack_python_cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'importlib-metadata>=6.0.0,<7.0.0',
 'rich>=13.3.2,<14.0.0',
 'youtrack-python-openapi>=2023.1,<2024.0']

entry_points = \
{'console_scripts': ['youtrack-cli = youtrack_python_cli.cli:cli']}

setup_kwargs = {
    'name': 'youtrack-python-cli',
    'version': '0.1.3',
    'description': 'Basic Youtrack CLI in python',
    'long_description': '[![GitHub](https://img.shields.io/badge/GitHub-noahp/youtrack--python--cli-8da0cb?style=for-the-badge&logo=github)](https://github.com/noahp/youtrack-python-cli)\n[![PyPI\nversion](https://img.shields.io/pypi/v/youtrack-python-cli.svg?style=for-the-badge&logo=PyPi&logoColor=white)](https://pypi.org/project/youtrack-python-cli/)\n[![PyPI\npyversions](https://img.shields.io/pypi/pyversions/youtrack-python-cli.svg?style=for-the-badge&logo=python&logoColor=white&color=ff69b4)](https://pypi.python.org/pypi/youtrack-python-cli/)\n[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/noahp/youtrack-python-cli/main.yml?branch=main&logo=github-actions&logoColor=white&style=for-the-badge)](https://github.com/noahp/youtrack-python-cli/actions)\n[![codecov](https://img.shields.io/codecov/c/github/noahp/youtrack-python-cli.svg?style=for-the-badge&logo=codecov)](https://codecov.io/gh/noahp/youtrack-python-cli)\n\n# YouTrack Python CLI\n\n## Installation\n\n```bash\n❯ pip install youtrack-python-cli\n# OR, if you use virtualenvs or conda envs in your working repo, use pipx:\n❯ pipx install youtrack-python-cli\n```\n\n## Configuration\n\nThe script needs a YouTrack URL to target API requests, and a token for auth.\n\n3 configuration methods:\n\n1. set into current repo\'s git config:\n\n   ```bash\n   ❯ git config youtrack.token "$YOUTRACK_TOKEN"\n   ❯ git config youtrack.url https://your-youtrack-server/api\n   ```\n\n2. set via environment variables, `YOUTRACK_URL` and `YOUTRACK_TOKEN`\n3. set via command line parameters, `--url` and `--token`\n\n## Usage\n\n### As git pre-push hook\n\nSee the [`pre-push`](pre-push) example, which can be copied directly into\n`.git/hooks/pre-push`. That example checks the commit title for the YouTrack\nticket ID as the first item, for example `EXAMPLE-1234 some commit title`.\n\n### Running standalone\n\n```bash\n❯ youtrack-cli --url "https://your-youtrack-server/api" --token $YOUTRACK_TOKEN get --confirm-prompt --ticket example-1234\n                                                  Issue data for example-1234\n┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n┃           Key ┃ Value                                                                                                     ┃\n┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩\n│    idReadable │ EXAMPLE-9377                                                                                              │\n├───────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────┤\n│       summary │ Test ticket title                                                                                         │\n├───────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────┤\n│ assignee_name │ Jane Doe                                                                                                  │\n├───────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────┤\n│ reporter_name │ jane                                                                                                      │\n├───────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────┤\n│   description │ Long description, truncated to max of 1024 characters                                                     │\n├───────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────┤\n│           url │ https://your-youtrack-server/issue/EXAMPLE-1234                                                           │\n└───────────────┴───────────────────────────────────────────────────────────────────────────────────────────────────────────┘\nType the ticket id to confirm: example-1234\n```\n\n## Development\n\n### Releasing\n\nManual. Steps are:\n\n```bash\n# 1. bump version, eg just the patch:\n❯ poetry version patch\nBumping version from 0.1.1 to 0.1.2\n# 2. store version for remaining commands\n❯ _VER=$(poetry version --short)\n# 3. Save version bump\n❯ git add . && git commit -m "Bump version to ${_VER}"\n# 4. Create annotated tag\n❯ git tag -a {-m=,}${_VER}\n# 5. Push\n❯ git push && git push --tags\n# 6. Build pypi release artifacts\n❯ rm -rf build && poetry build\n# 7. Publish\n❯ poetry publish --username=__token__ --password=$(<~/.noahp-pypi-pw)\n# 8. Github release stuff\n❯ gh release create --generate-notes ${_VER}\n```\n\nAnd all-in-one for copy paste:\n\n```bash\npoetry version patch \\\n  && _VER=$(poetry version --short) \\\n  && git add . \\\n  && git commit -m "Bump version to ${_VER}" \\\n  && git tag -a {-m=,}${_VER} \\\n  && git push && git push --tags \\\n  && rm -rf build && poetry build \\\n  && poetry publish --username=__token__ --password=$(<~/.noahp-pypi-pw) \\\n  && gh release create --generate-notes ${_VER}\n```\n',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
