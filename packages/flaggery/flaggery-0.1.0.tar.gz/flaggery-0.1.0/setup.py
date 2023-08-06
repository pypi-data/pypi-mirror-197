# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flaggery',
 'flaggery.api',
 'flaggery.api.routers',
 'flaggery.db',
 'flaggery.db.migrations',
 'flaggery.db.migrations.versions']

package_data = \
{'': ['*']}

install_requires = \
['alembic>=1.9.4,<2.0.0',
 'cassandra-driver>=3.25.0,<4.0.0',
 'fastapi>=0.92.0,<0.93.0',
 'gunicorn>=20.1.0,<21.0.0',
 'jinja2>=3.1.2,<4.0.0',
 'merge-args>=0.1.5,<0.2.0',
 'pydantic>=1.10.5,<2.0.0',
 'pyyaml>=6.0,<7.0',
 'sqlalchemy>=2.0.4,<3.0.0',
 'uvicorn>=0.20.0,<0.21.0']

entry_points = \
{'flaggery.plugins.cache': ['flaggery.cache.MemoryCache = '
                            'flaggery.cache.MemoryCache']}

setup_kwargs = {
    'name': 'flaggery',
    'version': '0.1.0',
    'description': 'Feature flag management framework for serving rollouts, ab-tests and feature groups',
    'long_description': '\n# Flaggery\n\nFeature flag management framework for serving rollouts, ab-tests and feature groups.\n\n### Installation\n\n```bash\npip install flaggery\n```\n\n### Starting the Rest API server\n\n```bash\nuvicorn --host <host> --port <port> flaggery.api.main:app\n```\n\n### Rest API Reference\n\nTo access the API documentation,\nfirst start the API server and then open\n[http://{hostname}:{port}/docs](http://localhost/docs)\nin your browser.\n\n### Configuring the API server\n\nThe API server can be configured by setting the following environment variables:\n\n| Variable                   | Required | Defaut | Description                                                                                                                                                                                                                                                                                                                                                                                                                              |\n|----------------------------|----------|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|\n| `FLAGGERY_DB_URL`          | Yes      | -      | SQLAlchemy compatible connection URL for an existing database.<br><br>Obs: Depending on which database you use, you might also need to install database-specific Python clients (e.g.: psycopg2 for PostgreSQL)                                                                                                                                                                                                                          |\n| `FLAGGERY_DB_AUTO_UPGRADE` | No       | False  | If True, database will be migrated to the latest schema on server startup.                                                                                                                                                                                                                                                                                                                                                               |\n| `FLAGGERY_ADMIN_MODE`      | No       | False  | If True, all endpoints are available. <br> <br> If false, the server goes on a limited read-only mode, in which all endpoints are locked except for `GET /v1/subject/flags` <br> <br> For both security and performance reasons, it is recommended to deploy a single replica of the server in admin mode, which can only be accessed by admins, and many replicas in limited read-only mode, which can be accessed by clients at scale. |\n\n[//]: # (Deploying with Docker)\n[//]: # (Deploying with Helm)\n[//]: # (Data model)\n[//]: # (Thumbnail)\n[//]: # (Table of contents)\n',
    'author': 'Lariel Fernandes',
    'author_email': 'lariel.c2.fernandes@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/lariel.fernandes/flaggery',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
