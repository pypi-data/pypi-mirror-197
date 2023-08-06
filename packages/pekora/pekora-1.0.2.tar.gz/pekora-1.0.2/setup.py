# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pekora']

package_data = \
{'': ['*']}

install_requires = \
['alianator>=4.0.2,<5.0.0',
 'colour>=0.1.5,<0.2.0',
 'decorator>=5.1.1,<6.0.0',
 'inflect>=6.0.2,<7.0.0',
 'inquirerpy>=0.3.4,<0.4.0',
 'py-cord>=2.4.0,<3.0.0',
 'pyperclip==1.8.1',
 'typer[all]>=0.7.0,<0.8.0',
 'yarl>=1.8.2,<2.0.0']

entry_points = \
{'console_scripts': ['pekora = pekora.cli:app']}

setup_kwargs = {
    'name': 'pekora',
    'version': '1.0.2',
    'description': 'A command-line calculator for Discord permission values',
    'long_description': "# Pekora\n\n[![PyPI](https://img.shields.io/pypi/v/pekora?logo=pypi&color=green&logoColor=white&style=for-the-badge)](https://pypi.org/project/pekora)\n[![PyPI - License](https://img.shields.io/pypi/l/pekora?color=03cb98&style=for-the-badge)](https://github.com/celsiusnarhwal/pekora/blob/main/LICENSE.md)\n[![Code style: Black](https://aegis.celsiusnarhwal.dev/badge/black?style=for-the-badge)](https://github.com/psf/black)\n\nPekora is a calculator for Discord permission values. With it, you can calculate permission values, see detailed\ninformation about the permissions a value represents, and interactively build your own\npermissions.\n\n## Installation\n\n### pipx (recommended)\n\n[Install pipx](https://pypa.github.io/pipx/installation/), then run:\n\n```bash\npipx install pekora\n```\n\n### Homebrew (macOS and Linux only)\n\n[Homebrew](https://brew.sh) users can install Pekora from the\n[Houkago Tea Tap](https://github.com/celsiusnarhwal/homebrew-htt).\n\n```bash\nbrew tap celsiusnarhwal/htt\nbrew install pekora\n```\n\n## Documentation\n\nFor documentation, including usage instructions, visit [Pekora's website](https://pekora.celsiusnarhwal.dev).\n\n## License\n\nPekora is licensed under the [MIT License](https://github.com/celsiusnarhwal/pekora/blob/main/LICENSE.md). Its\ndocumentation is licensed under [CC BY 4.0](https://pekora.celsiusnarhwal.dev/license).\n",
    'author': 'celsius narhwal',
    'author_email': 'hello@celsiusnarhwal.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pekora.celsiusnarhwal.dev',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
