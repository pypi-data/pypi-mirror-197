
# Flaggery

Feature flag management framework for serving rollouts, ab-tests and feature groups.

### Installation

```bash
pip install flaggery
```

### Starting the Rest API server

```bash
uvicorn --host <host> --port <port> flaggery.api.main:app
```

### Rest API Reference

To access the API documentation,
first start the API server and then open
[http://{hostname}:{port}/docs](http://localhost/docs)
in your browser.

### Configuring the API server

The API server can be configured by setting the following environment variables:

| Variable                   | Required | Defaut | Description                                                                                                                                                                                                                                                                                                                                                                                                                              |
|----------------------------|----------|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `FLAGGERY_DB_URL`          | Yes      | -      | SQLAlchemy compatible connection URL for an existing database.<br><br>Obs: Depending on which database you use, you might also need to install database-specific Python clients (e.g.: psycopg2 for PostgreSQL)                                                                                                                                                                                                                          |
| `FLAGGERY_DB_AUTO_UPGRADE` | No       | False  | If True, database will be migrated to the latest schema on server startup.                                                                                                                                                                                                                                                                                                                                                               |
| `FLAGGERY_ADMIN_MODE`      | No       | False  | If True, all endpoints are available. <br> <br> If false, the server goes on a limited read-only mode, in which all endpoints are locked except for `GET /v1/subject/flags` <br> <br> For both security and performance reasons, it is recommended to deploy a single replica of the server in admin mode, which can only be accessed by admins, and many replicas in limited read-only mode, which can be accessed by clients at scale. |

[//]: # (Deploying with Docker)
[//]: # (Deploying with Helm)
[//]: # (Data model)
[//]: # (Thumbnail)
[//]: # (Table of contents)
