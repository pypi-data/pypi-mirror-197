# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djangocms_htmlsitemap', 'djangocms_htmlsitemap.migrations']

package_data = \
{'': ['*'],
 'djangocms_htmlsitemap': ['locale/fr/LC_MESSAGES/*',
                           'templates/djangocms_htmlsitemap/*']}

install_requires = \
['Django>=1.11,<4', 'django-cms>=3.8']

setup_kwargs = {
    'name': 'djangocms-htmlsitemap',
    'version': '1.0.0',
    'description': 'A Django CMS plugin for building HTML sitemaps showing organized lists of CMS pages.',
    'long_description': "# djangocms-htmlsitemap\n\n[![Latest Version](http://img.shields.io/pypi/v/djangocms-htmlsitemap.svg?style=flat-square)](https://pypi.python.org/pypi/djangocms-htmlsitemap/)\n[![License](http://img.shields.io/pypi/l/djangocms-htmlsitemap.svg?style=flat-square)](https://pypi.python.org/pypi/djangocms-htmlsitemap/)\n\n\n*A Django CMS plugin for building HTML sitemaps showing organized lists of CMS pages.*\n\n## Requirements\n\nPython 3.8.1+, Django 1.11+, Django-CMS 3.8+.\n\n## Installation\n\nJust run:\n```sh\npip install djangocms-htmlsitemap\n```\n\nOnce installed you just need to add `djangocms_htmlsitemap` to `INSTALLED_APPS` in your project's settings module:\n```py\nINSTALLED_APPS = (\n    # other apps\n    'djangocms_htmlsitemap',\n)\n```\n\nThen install the models:\n```py\npython manage.py migrate djangocms_htmlsitemap\n```\n\n*Congrats! You’re in.*\n\n## Authors\n\nKapt <dev@kapt.mobi> and [contributors](https://github.com/kapt-labs/djangocms-htmlsitemap/contributors)\n\n## License\n\nBSD. See `LICENSE` for more details.\n",
    'author': 'Kapt dev team',
    'author_email': 'dev@kapt.mobi',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/kapt/open-source/djangocms-htmlsitemap',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
