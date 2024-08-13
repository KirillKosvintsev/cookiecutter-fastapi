# Python Packages Project Generator

## Set up

```bash
cookiecutter gh:kosvintsevke/cookiecutter-fastapi
```

## Features

In this [cookiecutter 🍪](https://github.com/cookiecutter/cookiecutter) template we combine state-of-the-art libraries
and best development practices for Python.

### Development features

- Supports `Python 3.8` and higher.
- [`Poetry`](https://python-poetry.org/) as a dependency manager. See configuration
  in [`pyproject.toml`](%7B%7B%20cookiecutter.project_name.lower().replace('%20',%20'-')%20%7D%7D/pyproject.toml).
- Automatic codestyle with [`Ruff formatter`](https://docs.astral.sh/ruff/formatter/)
- Linting with [`ruff`](https://github.com/astral-sh/ruff)
- Type checks with [`mypy`](https://mypy.readthedocs.io), security checks
  with [`safety`](https://github.com/pyupio/safety).
- Dependencies check with [`deptry`](https://deptry.com/)
- Testing with [`pytest`](https://docs.pytest.org/en/latest/) and [`coverage`](https://github.com/nedbat/coveragepy).
- Ready-to-use [`pre-commit`](https://pre-commit.com/) hooks with code-formatting.
- Ready-to-use [`.editorconfig`](%7B%7B%20cookiecutter.project_name.lower().replace('%20',%20'-')%20%7D%7D/.editorconfig), [`.dockerignore`](%7B%7B%20cookiecutter.project_name.lower().replace('%20',%20'-')%20%7D%7D/.dockerignore),
and [`.gitignore`](%7B%7B%20cookiecutter.project_name.lower().replace('%20',%20'-')%20%7D%7D/.gitignore).

### Code template features

- [`ml`](%7B%7B%20cookiecutter.project_name.lower().replace('%20',%20'-')%20%7D%7D/ml) folder with example ML scripts for data preparation scripts, learning and storing models etc.
- [`app`](%7B%7B%20cookiecutter.project_name.lower().replace('%20',%20'-')%20%7D%7D/app) folder with optional FastAPI app template (api, schemas, repositories, services, models, gateways).
- Dynamic [templates](%7B%7B%20cookiecutter.project_name.lower().replace('%20',%20'-')%20%7D%7D/app/db) for SqlAlchemy, SQLModel or Beanie ORMs and SqlAlchemy templates for SQL Scripts.
- Basic [`gateways`](%7B%7B%20cookiecutter.project_name.lower().replace('%20',%20'-')%20%7D%7D/app/gateways) scripts for different tasks.
- [Configuration](%7B%7B%20cookiecutter.project_name.lower().replace('%20',%20'-')%20%7D%7D/app/config/config.py) management supports ENVIRONMENT, `.env` and `dev.yaml` sources.
- Bacis [`core`](%7B%7B%20cookiecutter.project_name.lower().replace('%20',%20'-')%20%7D%7D/app/core) functionalities for security, logging, cache, MQ, Celery and other tasks.

### Deployment features

- `Github Actions` with linters and tests in
  the [workflow](%7B%7B%20cookiecutter.project_name.lower().replace('%20',%20'-')%20%7D%7D/.github/workflows/%7B%7B%20cookiecutter.package_name%20%7D%7D.yml).
- `Gitlab CI` with linters and tests in
  the [pipeline](%7B%7B%20cookiecutter.project_name.lower().replace('%20',%20'-')%20%7D%7D/.gitlab-ci.yml).
  Click [here](pages/gitlab.md) for detailed overview.
- Ready-to-use [`Makefile`](%7B%7B%20cookiecutter.project_name.lower().replace('%20',%20'-')%20%7D%7D/Makefile) with
  formatting, linting, and testing. More details in [makefile-usage](#makefile-usage).
- [`Dockerfile`](%7B%7B%20cookiecutter.project_name.lower().replace('%20',%20'-')%20%7D%7D/Dockerfile) for your package.
- [`docker-compose.yml`](%7B%7B%20cookiecutter.project_name.lower().replace('%20',%20'-')%20%7D%7D/docker-compose.yml) for
  local development in Docker.
- Dynamic [`pyproject.toml`](%7B%7B%20cookiecutter.project_name.lower().replace('%20',%20'-')%20%7D%7D/pyproject.toml).


## How to use it

### Installation

To begin using the template consider updating `cookiecutter`

```bash
pip install -U cookiecutter
```

then go to a directory where you want to create your project and run:

```bash
cookiecutter gh:kosvintsevke/cookiecutter-fastapi
```

### Input variables

Template generator will ask you to fill some variables.

The input variables, with their default values:

| **Parameter**         | **Default value**                                      | **Description**                                                                                              |
|:---------------------:|:------------------------------------------------------:|--------------------------------------------------------------------------------------------------------------|
| `project_name`        | `python-project`                                       | [Check the availability of possible name](http://ivantomic.com/projects/ospnc/) before creating the project. |
| `package_name`        | based on the `project_name`                            | Name of the python package with source code                                                                  |
| `python_version`      | `3.9`                                                  | Python version. One of `3.8`, `3.9`, `3.10`, `3.11`, `3.12`. It is used for builds, CI and formatters.       |
| `project_type`        | `fastapi_app`                                          | Type of project. Either `fastapi_app` or `empty`.                                                            |
| `db_option`           | `none`                                                 | Database option. One of `none`, `sqlalchemy_orm`, `sqlalchemy_queries`, `sqlmodel`, `beanie`.                |
| `include_ml_exp_folder` | `n`                                                  | Whether to include ML experiment folder. Either `y` or `n`.                                                  |
| `ci_git_platform`     | `none`                                                 | Git platform for CI. One of `none`, `github`, `gitlab`.                                                      |
| `git_username`        | `username` (if `ci_git_platform` is not `none`)        | User or organization name for Git platform                                                                   |
| `git_repo_url`        | based on `ci_git_platform`, `project_name` and `username` | URL to the git repository                                                                                    |

All input values will be saved in the `.cookiecutterrc` file so that you won't lose them. 😉

#### Notes:

1. The `project_type` determines the initial structure of your project:
   - `fastapi_app`: Sets up a FastAPI application structure.
   - `empty`: Creates a minimal project structure with just a `run.py` file.

2. The `db_option` is only applicable when `project_type` is set to `fastapi_app`. It determines the database setup:
   - `none`: No database setup.
   - `sqlalchemy_orm`: Sets up SQLAlchemy with ORM.
   - `sqlalchemy_queries`: Sets up SQLAlchemy for raw SQL queries.
   - `sqlmodel`: Sets up SQLModel.
   - `beanie`: Sets up Beanie for MongoDB.

3. The `include_ml_exp_folder` option adds a folder for machine learning experiments if set to `y`.

4. The `ci_git_platform` option sets up CI configuration:
   - `none`: No CI setup.
   - `github`: Sets up GitHub Actions.
   - `gitlab`: Sets up GitLab CI.

5. The `git_username` and `git_repo_url` are only prompted if `ci_git_platform` is not `none`.
#### Demo

[![Demo of github.com/TezRomacH/python-package-template](https://asciinema.org/a/422052.svg)](https://asciinema.org/a/422052)

### More details

Your project will contain `README.md` file with instructions for development, deployment, etc. You can
read [the project README.md template](%7B%7B%20cookiecutter.project_name.lower().replace('%20',%20'-')%20%7D%7D/README.md)
before.

### Initial set up

#### Initialize `poetry`

By running `make install`

After you create a project, it will appear in your directory, and will
display [a message about how to initialize the project](%7B%7B%20cookiecutter.project_name.lower().replace('%20',%20'-')%20%7D%7D/README.md#installation).

#### Initialize `pre-commit`

By running `make pre-commit-install`. Make sure to set up git first via `git init`.

### Makefile usage

[`Makefile`](%7B%7B%20cookiecutter.project_name.lower().replace('%20',%20'-')%20%7D%7D/Makefile)
contains a lot of functions
for faster development.

<details>
<summary>1. Download and remove Poetry</summary>
<p>

To download and install Poetry run:

```bash
make poetry-download
```

To uninstall

```bash
make poetry-remove
```

</p>
</details>

<details>
<summary>2. Install all dependencies and pre-commit hooks</summary>
<p>

Install requirements:

```bash
make install
```

Pre-commit hooks coulb be installed after `git init` via

```bash
make pre-commit-install
```

</p>
</details>

<details>
<summary>3. Codestyle</summary>
<p>

Automatic formatting uses `ruff` formatter

```bash
make codestyle

# or use synonym
make format
```

Codestyle checks only, without rewriting files:

```bash
make check-codestyle
```

Update all dev libraries to the latest version using one comand

```bash
make update-dev-deps
```

</p>
</details>

<details>
<summary>4. Code security</summary>
<p>

```bash
make check-safety
```

This command launches `Poetry` integrity checks as well as identifies security issues with `Safety`

```bash
make check-safety
```

</p>
</details>

<details>
<summary>5. Type checks</summary>
<p>

Run `mypy` static type checker

```bash
make mypy
```

</p>
</details>

<details>
<summary>6. Tests with coverage</summary>
<p>

Run `pytest`

```bash
make test
```

</p>
</details>

<details>
<summary>7. All linters</summary>
<p>

Of course there is a command to ~~rule~~ run all linters in one:

```bash
make lint
```

</p>
</details>

<details>
<summary>8. Docker</summary>
<p>

Build image:

```bash
make docker-build
```

Which is equivalent to:

```bash
make docker-build VERSION=latest
```

Remove docker image with:

```bash
make docker-remove
```

Run docker container with:

```bash
make docker-up
```

Stop docker container with:

```bash
make docker-down
```

Run docker container in detach (-d) mode with:

```bash
make docker-debug
```

Also, you can run **poetry directly**:

```bash
make local-up
```

</p>
</details>

<details>
<summary>9. Cleanup</summary>
<p>
Delete cache and build files:

```bash
make cleanup
```

</p>
</details>

### Project structure

The repository is organized as follows:

```
.
├── Dockerfile              - Docker configuration for containerization
├── Makefile                - Makefile with common commands for development
├── README.md               - Project documentation
├── app/                    - Main application directory
│   ├── api/                - API-related code
│   │   ├── events.py       - Event handlers for the API
│   │   ├── middleware.py   - Middleware for API requests
│   │   ├── system.py       - System-level API endpoints
│   │   └── v1/             - Version 1 of the API
│   │       ├── api_router.py  - Main API router
│   │       └── example_router.py  - Example router for specific endpoints
│   ├── config/             - Configuration management
│   │   ├── config.py       - Configuration setup
│   │   ├── dotenv/         - Directory for .env files
│   │   └── yaml/           - YAML configuration files
│   │       └── dev.yaml    - Development configuration
│   ├── core/               - Core functionality
│   │   ├── cache.py        - Caching mechanisms
│   │   ├── celery_app.py   - Celery configuration for async tasks
│   │   ├── dependencies.py - Dependency injection setup
│   │   ├── errors.py       - Custom error handling
│   │   ├── logger.py       - Logging configuration
│   │   ├── message_queue.py - Message queue integration
│   │   ├── paginator.py    - Pagination utilities
│   │   ├── security.py     - Security-related functions
│   │   └── utils.py        - General utility functions
│   ├── db/                 - Database-related code
│   │   ├── beanie/         - Beanie (MongoDB) specific code
│   │   ├── sqlalchemy/     - SQLAlchemy specific code
│   │   │   ├── alembic.ini - Alembic configuration for migrations
│   │   │   ├── migrations/ - Database migrations
│   │   │   ├── queries.py  - SQL queries
│   │   │   └── session.py  - Database session management
│   │   └── sqlmodel/       - SQLModel specific code
│   ├── gateways/           - External service integrations
│   ├── main.py             - Main application entry point
│   ├── models/             - Data models
│   │   ├── beanie/         - Beanie models
│   │   ├── sqlalchemy/     - SQLAlchemy models
│   │   └── sqlmodel/       - SQLModel models
│   ├── repositories/       - Data access layer
│   │   ├── beanie/         - Beanie repositories
│   │   ├── sqlalchemy/     - SQLAlchemy repositories
│   │   └── sqlmodel/       - SQLModel repositories
│   ├── schemas/            - Pydantic schemas
│   └── services/           - Business logic layer
├── docker-compose.yml      - Docker Compose configuration
├── ml/                     - Machine Learning related code
│   ├── data/               - Data processing scripts
│   ├── models/             - ML model definitions and saved models
│   ├── notebooks/          - Jupyter notebooks for analysis
│   ├── preprocessing/      - Data preprocessing scripts
│   └── training/           - Model training scripts
├── pyproject.toml          - Python project configuration (Poetry)
├── run.py                  - Script to run the application
└── tests/                  - Test suite
    ├── api/                - API tests
    ├── conftest.py         - pytest configuration
    └── unit/               - Unit tests
```

### Key Components:

1. **app/**: Contains the main application code.
   - **api/**: Handles API-related functionality, including routing and versioning.
   - **config/**: Manages application configuration.
   - **core/**: Provides core functionality like caching, logging, and security.
   - **db/**: Contains database-related code, supporting multiple ORMs.
   - **models/**: Defines data models for different ORMs.
   - **repositories/**: Implements the data access layer.
   - **services/**: Contains business logic.

2. **ml/**: Houses machine learning-related code and resources.

3. **tests/**: Contains all test files, separated into API and unit tests.

4. **Dockerfile** and **docker-compose.yml**: Provide containerization support.

5. **pyproject.toml**: Defines project dependencies and configuration.

This structure supports a modular, maintainable, and scalable application, with clear separation of concerns and support for multiple database technologies and machine learning integration.

## 🏅 Acknowledgements

This template was initially forked from the following template:

- https://github.com/TezRomacH/python-package-template

Other useful templates:

- https://github.com/Buuntu/fastapi-react
- https://github.com/nickatnight/cookiecutter-fastapi-backend
- https://github.com/arthurhenrique/cookiecutter-fastapi
- https://github.com/a1d4r/python-project-template