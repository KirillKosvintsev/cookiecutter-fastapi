# {{ cookiecutter.project_name.replace('-', ' ').replace('_', ' ') }}

## Установка

1. Клонируйте репозиторий `git`:

```bash
git clone {{ cookiecutter.git_repo_url }}.git
cd {{ cookiecutter.project_name.lower().replace(' ', '-') }}
```

2. Если у вас не установлен `Poetry`, выполните:

```bash
make poetry-download
```

3. Инициализируйте poetry и установите хуки `pre-commit`:

```bash
make install
make pre-commit-install
```

4. Запустите форматтеры, линтеры и тесты. Убедитесь, что нет ошибок.

```bash
make format lint test
```

### Использование Makefile

[`Makefile`]({{ cookiecutter.git_repo_url }}/blob/master/Makefile) содержит множество функций для ускорения разработки.

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

Автоматическое форматирование использует `ruff`.

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

Эта команда выявляет проблемы безопасности с помощью `Safety`:

```bash
make check-safety
```

Для проверки `pyproject.toml` используйте:

```bash
make check-poetry
```

</p>
</details>

<details>
<summary>5. Линтинг и проверки типов</summary>
<p>

Запуск статического линтинга с `ruff` и `mypy`:

```bash
make static-lint
```

</p>
</details>

<details>
<summary>6. Тесты с покрытием</summary>
<p>

Запуск тестов:

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
Удаление файлов pycache:

```bash
make pycache-remove
```

Удаление сборки пакета:

```bash
make build-remove
```

Удаление файлов .DS_STORE:

```bash
make dsstore-remove
```

Удаление .mypycache:

```bash
make mypycache-remove
```

Или для удаления всего вышеперечисленного выполните:

```bash
make cleanup
```

</p>
</details>

## Доступ к документации Swagger

> <http://localhost:8080/docs>

## Доступ к документации Redoc

> <http://localhost:8080/redoc>

## Благодарности

Этот проект был сгенерирован с помощью [`cookiecutter-fastapi`](https://github.com/kosvintsevke/cookiecutter-fastapi)
