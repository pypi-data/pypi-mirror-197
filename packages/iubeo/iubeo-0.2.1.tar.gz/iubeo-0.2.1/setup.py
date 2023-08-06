# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iubeo']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'iubeo',
    'version': '0.2.1',
    'description': 'Friendlier way to write your config.',
    'long_description': '[![Build Status](https://travis-ci.com/isik-kaplan/iubeo.svg?branch=master)](https://travis-ci.com/isik-kaplan/iubeo)\n[![PyPI - License](https://img.shields.io/pypi/l/iubeo.svg)](https://pypi.org/project/iubeo/)\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/iubeo.svg)](https://pypi.org/project/iubeo/)\n\n\n## What is *iubeo*?\n\nFriendlier way to write your config.\n\n## What is it good for?\n\nYou write how you want to read your config.\n\n```py\nfrom iubeo import config\n\ndef list_from_string(val):\n    return val.split(\',\')\n\nCONFIG = config(\n    {\n        \'DATABASE\': {\n            \'USER\': str,\n            \'PASSWORD\': str,\n            \'HOST\': str,\n            \'PORT\': str,\n        },\n        \'ALLOWED_HOSTS\': list_from_string,\n    },\n    # prefix = \'\',  # default\n    # sep = \'__\',  # default\n)\n```\n\nwith the above config, environment variables like\n\n```.env\nDATABASE__USER=example\nDATABASE__PASSWORD=example-password\nDATABASE__HOST=localhost\nDATABASE__PORT=5432\nALLOWED_HOSTS=example.com,api.example.com,www.example.com\n```\n\nare read from the environment.\n\n```py\nCONFIG.DATABASE.USER # "example-user"\nCONFIG.DATABASE.PASSWORD # "example-password"\nCONFIG.DATABASE.HOST # "localhost"\nCONFIG.DATABASE.PORT # "5432"\nCONFIG.ALLOWED_HOSTS # ["example.com", "api.example.com", "www.example.com"]\n```\n\nYou can also change the separator and add a prefix to manage your environment variables better\n\n```py\nCONFIG = config({\n    \'SECRETS\': {\n        \'API_KEY\': str,\n    },\n}, prefix=\'APP1\', sep=\'-\')\n```\nwhich would be read from\n```.env\nAPP1-SECRETS-API_KEY=isik_kaplan_api_key\n```\n\nIubeo also comes with a couple of pre-configured functions to read common environment variable types:\n```py\nfrom iubeo import config, comma_separated_list, boolean\n\nCONFIG = config({\n    \'DATABASE\': {\n        \'USER\': str,\n        \'PASSWORD\': str,\n        \'HOST\': str,\n        \'PORT\': str,\n    },\n    \'ALLOWED_HOSTS\': comma_separated_list,\n    \'DEBUG\': boolean,\n})\n```\n',
    'author': 'isik-kaplan',
    'author_email': 'isik.kaplan@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/isik-kaplan/iubeo',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
