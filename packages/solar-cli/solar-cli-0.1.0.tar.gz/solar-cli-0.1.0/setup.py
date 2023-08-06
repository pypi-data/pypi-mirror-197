# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['solar', 'solar.api', 'solar.cmd', 'solar.types']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.4,<4.0.0',
 'click>=8.1.3,<9.0.0',
 'more-itertools>=9.1.0,<10.0.0',
 'orjson>=3.8.7,<4.0.0',
 'pydantic>=1.10.6,<2.0.0',
 'rich>=13.3.2,<14.0.0']

entry_points = \
{'console_scripts': ['solar = solar.cli:cli']}

setup_kwargs = {
    'name': 'solar-cli',
    'version': '0.1.0',
    'description': 'CLI app for Solr',
    'long_description': '# Solar\n\nThis CLI tool provides help with some routine Solr operations:\n- Import / Export data\n- Import / Export configs\n- Re-index Collection (WIP)\n\n\n# Usage\n\n# Export\n\n## Export data\n\nThis command will save docs from `<collection>` to local folder `./data`:\n```sh\nsolar -c "<collection>" "https://<username>:<password>@localhost:8333" export ./data\n```\n\n### Export nested documents\nSolr can handle nested documents. To see nested structure of collection usually we add `fl="*, [child]"` to our query params. Solar can handle exporting nested documents by adding `--nested` flag:\n```sh\nsolar -c "<collection>" "https://<username>:<password>@localhost:8333" export --nested ./data\n```\n\n\n\n## Export config\n\nIf we want to save collection config, we can user `export-config` command:\n\n```sh\nsolar -c "<collection>" "https://<username>:<password>@localhost:8333" export-config ./configs\n```\nThis will all config files to local folder `./configs`\n\n# Import\n\n## Import data\n\nLater, we can import previously exported data with `import` command, and `./data/<collection>.json` as source file:\n```sh\nsolar "https://<username>:<password>@localhost:8333" export ./data/<collection>.json\n```\n\nWe do not have to specify collection name, source `.json` already have collection name. However, if we want to import data as collection with different name, we can set this with `-c` flag:\n```sh\nsolar -c "<new collection name>" "https://<username>:<password>@localhost:8333" export ./data/<collection>.json\n```\n\n## Import config\n\nSolar can help you import configsets to your Solr instance:\n```sh\nsolar -c "https://<username>:<password>@localhost:8333" import-config <config folder path>\n```\n\nThis command will read files from provide config path, zip them, and send to Solr. By default, created config name will be equal to config folder name. For example, if we import config from `./configs/products`, Solar will create config named `products`.\n\nIf we want to override default name, we can use `--name` flag:\n\n```sh\nsolar -c "https://<username>:<password>@localhost:8333" import-config --name "product-v2" <config folder path>\n```\n\nThis will create config `product-v2`.\n\nAlso, we can overwrite existing config with `--overwrite` flag\n> This flag will add `cleanup=true` and `overwrite=true` params to request for creating config. However it is recommended to create config with the *new* name, because in some cases, Solr caches fields types, and some changes of new config will not be applied. Goog practice is version control your configs and name them with version identifier (commit hash, for example)\n> Using this flag also requires that no collections is linked to this config\n\n```sh\nsolar -c "https://<username>:<password>@localhost:8333" import-config --overwrite <config folder path>\n```\n\n# Other\n\n## Remove config\n\nConfig `<config name>` can be removed from Solr with this command:\n\n```sh\nsolar -c "https://<username>:<password>@localhost:8333" remove-config "<config name>"\n\n```\n',
    'author': 'Andrey S.',
    'author_email': 'andrewsapw@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
