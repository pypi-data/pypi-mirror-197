# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybrook', 'pybrook.consumers', 'pybrook.examples']

package_data = \
{'': ['*'], 'pybrook': ['frontend/*', 'frontend/build/*']}

install_requires = \
['Pillow>=8.4.0,<9.0.0',
 'fastapi>=0.87.0,<0.88.0',
 'gunicorn>=20.1.0,<21.0.0',
 'httpx>=0.21.1,<0.22.0',
 'locust>=2.6.1,<3.0.0',
 'loguru>=0.5.3,<0.6.0',
 'orjson>=3.6.5,<4.0.0',
 'pandoc-crossref>=0.1.1,<0.2.0',
 'pydantic>=1.10.6,<2.0.0',
 'pytest>=6.2.5,<7.0.0',
 'redis[asyncio]>=4.5.1,<5.0.0',
 'uvicorn[standard]>=0.20.0,<0.21.0',
 'uvloop>=0.17.0,<0.18.0',
 'watchdog>=2.1.6,<3.0.0']

entry_points = \
{'console_scripts': ['pybrook = pybrook.__main__:main']}

setup_kwargs = {
    'name': 'pybrook',
    'version': '0.1.2',
    'description': '',
    'long_description': '\nDokumentacja w formacie HTML, zawierająca instrukcje konfiguracji środowiska i referencję w jezyku angielskim,\n znajduje się w katalogu docs_html.',
    'author': 'Michał Rokita',
    'author_email': 'mrokita@mrokita.pl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
