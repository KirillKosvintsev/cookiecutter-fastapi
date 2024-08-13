# Генератор проектов Python-пакетов

## Настройка

```bash
cookiecutter gh:kosvintsevke/cookiecutter-fastapi
```

## Особенности

В этом шаблоне [cookiecutter 🍪](https://github.com/cookiecutter/cookiecutter) мы объединяем современные библиотеки и лучшие практики разработки для Python.

### Особенности разработки

- Поддерживает `Python 3.8` и выше.
- [`Poetry`](https://python-poetry.org/) в качестве менеджера зависимостей. См. конфигурацию в [`pyproject.toml`](%7B%7B%20cookiecutter.project_name.lower().replace('%20',%20'-')%20%7D%7D/pyproject.toml).
- Автоматическое форматирование кода с [`Ruff formatter`](https://docs.astral.sh/ruff/formatter/)
- Линтинг с [`ruff`](https://github.com/astral-sh/ruff)
- Проверка типов с [`mypy`](https://mypy.readthedocs.io), проверка безопасности с [`safety`](https://github.com/pyupio/safety).
- Проверка зависимостей с [`deptry`](https://deptry.com/)
- Тестирование с [`pytest`](https://docs.pytest.org/en/latest/) и [`coverage`](https://github.com/nedbat/coveragepy).
- Готовые к использованию хуки [`pre-commit`](https://pre-commit.com/) с форматированием кода.
- Готовые к использованию [`.editorconfig`](%7B%7B%20cookiecutter.project_name.lower().replace('%20',%20'-')%20%7D%7D/.editorconfig), [`.dockerignore`](%7B%7B%20cookiecutter.project_name.lower().replace('%20',%20'-')%20%7D%7D/.dockerignore) и [`.gitignore`](%7B%7B%20cookiecutter.project_name.lower().replace('%20',%20'-')%20%7D%7D/.gitignore).

### Особенности шаблона кода

- Папка [`ml`](%7B%7B%20cookiecutter.project_name.lower().replace('%20',%20'-')%20%7D%7D/ml) с примерами скриптов ML для подготовки данных, обучения и сохранения моделей и т.д.
- Папка [`app`](%7B%7B%20cookiecutter.project_name.lower().replace('%20',%20'-')%20%7D%7D/app) с опциональным шаблоном приложения FastAPI (api, schemas, repositories, services, models, gateways).
- Динамические [шаблоны](%7B%7B%20cookiecutter.project_name.lower().replace('%20',%20'-')%20%7D%7D/app/db) для ORM SqlAlchemy, SQLModel или Beanie и шаблоны SqlAlchemy для SQL-скриптов.
- Базовые скрипты [`gateways`](%7B%7B%20cookiecutter.project_name.lower().replace('%20',%20'-')%20%7D%7D/app/gateways) для различных задач.
- [Конфигурация](%7B%7B%20cookiecutter.project_name.lower().replace('%20',%20'-')%20%7D%7D/app/config/config.py) поддерживает источники ENVIRONMENT, `.env` и `dev.yaml`.
- Базовый функционал [`core`](%7B%7B%20cookiecutter.project_name.lower().replace('%20',%20'-')%20%7D%7D/app/core) для безопасности, логирования, кэширования, MQ, Celery и других задач.

### Особенности развертывания

- `Github Actions` с линтерами и тестами в [рабочем процессе](%7B%7B%20cookiecutter.project_name.lower().replace('%20',%20'-')%20%7D%7D/.github/workflows/%7B%7B%20cookiecutter.package_name%20%7D%7D.yml).
- `Gitlab CI` с линтерами и тестами в [пайплайне](%7B%7B%20cookiecutter.project_name.lower().replace('%20',%20'-')%20%7D%7D/.gitlab-ci.yml). Нажмите [здесь](pages/gitlab.md) для подробного обзора.
- Готовый к использованию [`Makefile`](%7B%7B%20cookiecutter.project_name.lower().replace('%20',%20'-')%20%7D%7D/Makefile) с форматированием, линтингом и тестированием. Подробнее в [использовании makefile](#использование-makefile).
- [`Dockerfile`](%7B%7B%20cookiecutter.project_name.lower().replace('%20',%20'-')%20%7D%7D/Dockerfile) для вашего пакета.
- [`docker-compose.yml`](%7B%7B%20cookiecutter.project_name.lower().replace('%20',%20'-')%20%7D%7D/docker-compose.yml) для локальной разработки в Docker.
- Динамический [`pyproject.toml`](%7B%7B%20cookiecutter.project_name.lower().replace('%20',%20'-')%20%7D%7D/pyproject.toml).

## Как использовать

### Установка

Чтобы начать использовать шаблон, обновите `cookiecutter`:

```bash
pip install -U cookiecutter
```

затем перейдите в директорию, где вы хотите создать свой проект, и выполните:

```bash
cookiecutter gh:kosvintsevke/cookiecutter-fastapi
```

### Входные переменные

Генератор шаблонов попросит вас заполнить некоторые переменные.

Входные переменные с их значениями по умолчанию:

| **Параметр**           | **Значение по умолчанию**                             | **Описание**                                                                                                |
|:----------------------:|:-----------------------------------------------------:|-------------------------------------------------------------------------------------------------------------|
| `project_name`         | `python-project`                                      | [Проверьте доступность возможного имени](http://ivantomic.com/projects/ospnc/) перед созданием проекта.      |
| `package_name`         | на основе `project_name`                              | Имя python-пакета с исходным кодом                                                                           |
| `python_version`       | `3.9`                                                 | Версия Python. Одна из `3.8`, `3.9`, `3.10`, `3.11`, `3.12`. Используется для сборок, CI и форматтеров.      |
| `project_type`         | `fastapi_app`                                         | Тип проекта. Либо `fastapi_app`, либо `empty`.                                                               |
| `db_option`            | `none`                                                | Опция базы данных. Одна из `none`, `sqlalchemy_orm`, `sqlalchemy_queries`, `sqlmodel`, `beanie`.             |
| `include_ml_exp_folder`| `n`                                                   | Включать ли папку для ML-экспериментов. Либо `y`, либо `n`.                                                  |
| `ci_git_platform`      | `none`                                                | Git-платформа для CI. Одна из `none`, `github`, `gitlab`.                                                    |
| `git_username`         | `username` (если `ci_git_platform` не `none`)         | Имя пользователя или организации для Git-платформы                                                           |
| `git_repo_url`         | на основе `ci_git_platform`, `project_name` и `username` | URL к git-репозиторию                                                                                     |

Все входные значения будут сохранены в файле `.cookiecutterrc`, чтобы вы их не потеряли. 😉

#### Примечания:

1. `project_type` определяет начальную структуру вашего проекта:
   - `fastapi_app`: Настраивает структуру приложения FastAPI.
   - `empty`: Создает минимальную структуру проекта только с файлом `run.py`.

2. `db_option` применимо только когда `project_type` установлен в `fastapi_app`. Оно определяет настройку базы данных:
   - `none`: Без настройки базы данных.
   - `sqlalchemy_orm`: Настраивает SQLAlchemy с ORM.
   - `sqlalchemy_queries`: Настраивает SQLAlchemy для сырых SQL-запросов.
   - `sqlmodel`: Настраивает SQLModel.
   - `beanie`: Настраивает Beanie для MongoDB.

3. Опция `include_ml_exp_folder` добавляет папку для экспериментов машинного обучения, если установлена в `y`.

4. Опция `ci_git_platform` настраивает конфигурацию CI:
   - `none`: Без настройки CI.
   - `github`: Настраивает GitHub Actions.
   - `gitlab`: Настраивает GitLab CI.

5. `git_username` и `git_repo_url` запрашиваются только если `ci_git_platform` не `none`.

#### Демо

[![Демонстрация github.com/TezRomacH/python-package-template](https://asciinema.org/a/422052.svg)](https://asciinema.org/a/422052)

### Подробности

Ваш проект будет содержать файл `README.md` с инструкциями по разработке, развертыванию и т.д. Вы можете прочитать [шаблон README.md проекта](%7B%7B%20cookiecutter.project_name.lower().replace('%20',%20'-')%20%7D%7D/README.md) заранее.

### Начальная настройка

#### Инициализация `poetry`

Выполните `make install`

После создания проекта он появится в вашей директории и отобразит [сообщение о том, как инициализировать проект](%7B%7B%20cookiecutter.project_name.lower().replace('%20',%20'-')%20%7D%7D/README.md#installation).

#### Инициализация `pre-commit`

Выполните `make pre-commit-install`. Убедитесь, что сначала настроили git через `git init`.

### Использование Makefile

[`Makefile`](%7B%7B%20cookiecutter.project_name.lower().replace('%20',%20'-')%20%7D%7D/Makefile) содержит множество функций для ускорения разработки.

<details>
<summary>1. Загрузка и удаление Poetry</summary>
<p>

Для загрузки и установки Poetry выполните:

```bash
make poetry-download
```

Для удаления:

```bash
make poetry-remove
```

</p>
</details>

<details>
<summary>2. Установка всех зависимостей и хуков pre-commit</summary>
<p>

Установка требований:

```bash
make install
```

Хуки pre-commit могут быть установлены после `git init` через:

```bash
make pre-commit-install
```

</p>
</details>

<details>
<summary>3. Стиль кода</summary>
<p>

Автоматическое форматирование использует форматтер `ruff`:

```bash
make codestyle

# или используйте синоним
make format
```

Проверки стиля кода без перезаписи файлов:

```bash
make check-codestyle
```

Обновление всех dev-библиотек до последней версии одной командой:

```bash
make update-dev-deps
```

</p>
</details>

<details>
<summary>4. Безопасность кода</summary>
<p>

```bash
make check-safety
```

Эта команда запускает проверки целостности `Poetry`, а также выявляет проблемы безопасности с помощью `Safety`:

```bash
make check-safety
```

</p>
</details>

<details>
<summary>5. Проверки типов</summary>
<p>

Запуск статического анализатора типов `mypy`:

```bash
make mypy
```

</p>
</details>

<details>
<summary>6. Тесты с покрытием</summary>
<p>

Запуск `pytest`:

```bash
make test
```

</p>
</details>

<details>
<summary>7. Все линтеры</summary>
<p>

Конечно, есть команда для запуска всех линтеров сразу:

```bash
make lint
```

</p>
</details>

<details>
<summary>8. Docker</summary>
<p>

Сборка образа:

```bash
make docker-build
```

Что эквивалентно:

```bash
make docker-build VERSION=latest
```

Удаление docker-образа:

```bash
make docker-remove
```

Запуск docker-контейнера:

```bash
make docker-up
```

Остановка docker-контейнера:

```bash
make docker-down
```

Запуск docker-контейнера в режиме detach (-d):

```bash
make docker-debug
```

Также вы можете запустить **poetry напрямую**:

```bash
make local-up
```

</p>
</details>

<details>
<summary>9. Очистка</summary>
<p>
Удаление кэша и файлов сборки:

```bash
make cleanup
```

</p>
</details>

### Структура проекта

Репозиторий организован следующим образом:

```
.
├── Dockerfile              - Конфигурация Docker для контейнеризации
├── Makefile                - Makefile с общими командами для разработки
├── README.md               - Документация проекта
├── app/                    - Основная директория приложения
│   ├── api/                - Код, связанный с API
│   │   ├── events.py       - Обработчики событий для API
│   │   ├── middleware.py   - Промежуточное ПО для API-запросов
│   │   ├── system.py       - Системные конечные точки API
│   │   └── v1/             - Версия 1 API
│   │       ├── api_router.py  - Основной маршрутизатор API
│   │       └── example_router.py  - Пример маршрутизатора для конкретных конечных точек
│   ├── config/             - Управление конфигурацией
│   │   ├── config.py       - Настройка конфигурации
│   │   ├── dotenv/         - Директория для файлов .env
│   │   └── yaml/           - YAML файлы конфигурации
│   │       └── dev.yaml    - Конфигурация для разработки
│   ├── core/               - Основной функционал
│   │   ├── cache.py        - Механизмы кэширования
│   │   ├── celery_app.py   - Конфигурация Celery для асинхронных задач
│   │   ├── dependencies.py - Настройка инъекции зависимостей
│   │   ├── errors.py       - Обработка пользовательских ошибок
│   │   ├── logger.py       - Конфигурация логирования
│   │   ├── message_queue.py - Интеграция очереди сообщений
│   │   ├── paginator.py    - Утилиты для пагинации
│   │   ├── security.py     - Функции, связанные с безопасностью
│   │   └── utils.py        - Общие служебные функции
│   ├── db/                 - Код, связанный с базой данных
│   │   ├── beanie/         - Код, специфичный для Beanie (MongoDB)
│   │   ├── sqlalchemy/     - Код, специфичный для SQLAlchemy
│   │   │   ├── alembic.ini - Конфигурация Alembic для миграций
│   │   │   ├── migrations/ - Миграции базы данных
│   │   │   ├── queries.py  - SQL-запросы
│   │   │   └── session.py  - Управление сессиями базы данных
│   │   └── sqlmodel/       - Код, специфичный для SQLModel
│   ├── gateways/           - Интеграции с внешними сервисами
│   ├── main.py             - Основная точка входа в приложение
│   ├── models/             - Модели данных
│   │   ├── beanie/         - Модели Beanie
│   │   ├── sqlalchemy/     - Модели SQLAlchemy
│   │   └── sqlmodel/       - Модели SQLModel
│   ├── repositories/       - Слой доступа к данным
│   │   ├── beanie/         - Репозитории Beanie
│   │   ├── sqlalchemy/     - Репозитории SQLAlchemy
│   │   └── sqlmodel/       - Репозитории SQLModel
│   ├── schemas/            - Схемы Pydantic
│   └── services/           - Слой бизнес-логики
├── docker-compose.yml      - Конфигурация Docker Compose
├── ml/                     - Код, связанный с машинным обучением
│   ├── data/               - Скрипты обработки данных
│   ├── models/             - Определения ML-моделей и сохраненные модели
│   ├── notebooks/          - Jupyter-ноутбуки для анализа
│   ├── preprocessing/      - Скрипты предобработки данных
│   └── training/           - Скрипты обучения моделей
├── pyproject.toml          - Конфигурация Python-проекта (Poetry)
├── run.py                  - Скрипт для запуска приложения
└── tests/                  - Набор тестов
    ├── api/                - Тесты API
    ├── conftest.py         - Конфигурация pytest
    └── unit/               - Модульные тесты
    
```

### Ключевые компоненты:

1. **app/**: Содержит основной код приложения.
   - **api/**: Обрабатывает функциональность, связанную с API, включая маршрутизацию и версионирование.
   - **config/**: Управляет конфигурацией приложения.
   - **core/**: Предоставляет основной функционал, такой как кэширование, логирование и безопасность.
   - **db/**: Содержит код, связанный с базой данных, поддерживая несколько ORM.
   - **models/**: Определяет модели данных для различных ORM.
   - **repositories/**: Реализует слой доступа к данным.
   - **services/**: Содержит бизнес-логику.

2. **ml/**: Содержит код и ресурсы, связанные с машинным обучением.

3. **tests/**: Содержит все тестовые файлы, разделенные на API и модульные тесты.

4. **Dockerfile** и **docker-compose.yml**: Обеспечивают поддержку контейнеризации.

5. **pyproject.toml**: Определяет зависимости проекта и конфигурацию.

Эта структура поддерживает модульное, поддерживаемое и масштабируемое приложение с четким разделением задач и поддержкой нескольких технологий баз данных и интеграции машинного обучения.

## 🏅 Благодарности

Этот шаблон изначально был форкнут из следующего шаблона:

- https://github.com/a1d4r/python-project-template

Другие полезные шаблоны:

- https://github.com/TezRomacH/python-package-template
- https://github.com/Buuntu/fastapi-react
- https://github.com/nickatnight/cookiecutter-fastapi-backend
- https://github.com/arthurhenrique/cookiecutter-fastapi