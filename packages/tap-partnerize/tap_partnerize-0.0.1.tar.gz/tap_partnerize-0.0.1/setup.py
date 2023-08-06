# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_partnerize']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0', 'singer-sdk>=0.21.0,<0.22.0']

extras_require = \
{'s3': ['fs-s3fs>=1.1.1,<2.0.0']}

entry_points = \
{'console_scripts': ['tap-partnerize = tap_partnerize.tap:TapPartnerize.cli']}

setup_kwargs = {
    'name': 'tap-partnerize',
    'version': '0.0.1',
    'description': '`tap-partnerize` is a Singer tap for Partnerize, built with the Meltano Singer SDK.',
    'long_description': '# tap-partnerize\n\n`tap-partnerize` is a Singer tap for Partnerize.\n\nBuilt with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.\n\n<!--\n\nDeveloper TODO: Update the below as needed to correctly describe the install procedure. For instance, if you do not have a PyPi repo, or if you want users to directly install from your git repo, you can modify this step as appropriate.\n\n## Installation\n\nInstall from PyPi:\n\n```bash\npipx install tap-partnerize\n```\n\nInstall from GitHub:\n\n```bash\npipx install git+https://github.com/ORG_NAME/tap-partnerize.git@main\n```\n\n-->\n\n## Configuration\n\n### Accepted Config Options\n\n<!--\nDeveloper TODO: Provide a list of config options accepted by the tap.\n\nThis section can be created by copy-pasting the CLI output from:\n\n```\ntap-partnerize --about --format=markdown\n```\n-->\n\nA full list of supported settings and capabilities for this\ntap is available by running:\n\n```bash\ntap-partnerize --about\n```\n\n### Configure using environment variables\n\nThis Singer tap will automatically import any environment variables within the working directory\'s\n`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching\nenvironment variable is set either in the terminal context or in the `.env` file.\n\n### Source Authentication and Authorization\n\n<!--\nDeveloper TODO: If your tap requires special access on the source system, or any special authentication requirements, provide those here.\n-->\n\n## Usage\n\nYou can easily run `tap-partnerize` by itself or in a pipeline using [Meltano](https://meltano.com/).\n\n### Executing the Tap Directly\n\n```bash\ntap-partnerize --version\ntap-partnerize --help\ntap-partnerize --config CONFIG --discover > ./catalog.json\n```\n\n## Developer Resources\n\nFollow these instructions to contribute to this project.\n\n### Initialize your Development Environment\n\n```bash\npipx install poetry\npoetry install\n```\n\n### Create and Run Tests\n\nCreate tests within the `tap_partnerize/tests` subfolder and\n  then run:\n\n```bash\npoetry run pytest\n```\n\nYou can also test the `tap-partnerize` CLI interface directly using `poetry run`:\n\n```bash\npoetry run tap-partnerize --help\n```\n\n### Testing with [Meltano](https://www.meltano.com)\n\n_**Note:** This tap will work in any Singer environment and does not require Meltano.\nExamples here are for convenience and to streamline end-to-end orchestration scenarios._\n\n<!--\nDeveloper TODO:\nYour project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any "TODO" items listed in\nthe file.\n-->\n\nNext, install Meltano (if you haven\'t already) and any needed plugins:\n\n```bash\n# Install meltano\npipx install meltano\n# Initialize meltano within this directory\ncd tap-partnerize\nmeltano install\n```\n\nNow you can test and orchestrate using Meltano:\n\n```bash\n# Test invocation:\nmeltano invoke tap-partnerize --version\n# OR run a test `elt` pipeline:\nmeltano elt tap-partnerize target-jsonl\n```\n\n### SDK Dev Guide\n\nSee the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to\ndevelop your own taps and targets.\n',
    'author': 'Omar Abed',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.12',
}


setup(**setup_kwargs)
