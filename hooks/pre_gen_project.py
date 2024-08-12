"""This module is called before project is created."""

import re
import sys

PACKAGE_NAME = "{{ cookiecutter.package_name }}"
PYTHON_VERSION = "{{ cookiecutter.python_version }}"
PROJECT_TYPE = "{{ cookiecutter.project_type }}"
DB_OPTION = "{{ cookiecutter.db_option }}"
INCLUDE_ML_EXP_FOLDER = "{{ cookiecutter.include_ml_exp_folder }}"

MODULE_REGEX = re.compile(r"^[a-z][a-z0-9\-\_]+[a-z0-9]$")
PYTHON_VERSION_REGEX = re.compile(r"^3\.(8|9|10|11|12)$")


def validate_package_name(package_name: str) -> None:
    """Ensure that `package_name` parameter is valid.

    Valid inputs starts with the lowercase letter.
    Followed by any lowercase letters, numbers or underscores.

    Args:
        package_name: current project name

    Raises:
        ValueError: If project_name is not a valid Python module name
    """
    if MODULE_REGEX.fullmatch(package_name) is None:
        message = f"ERROR: The package name `{package_name}` is not a valid Python module name."
        raise ValueError(message)


def validate_python_version(python_version: str) -> None:
    """Validate the Python version."""
    if PYTHON_VERSION_REGEX.fullmatch(python_version) is None:
        message = f"ERROR: The Python version `{python_version}` is not valid. Choose from 3.8, 3.9, 3.10, 3.11, or 3.12."
        raise ValueError(message)


def validate_project_type(project_type: str) -> None:
    """Validate the project type."""
    if project_type not in ["fastapi_app", "empty"]:
        message = f"ERROR: The project type `{project_type}` is not valid. Choose either 'fastapi_app' or 'empty'."
        raise ValueError(message)


def validate_db_option(db_option: str) -> None:
    """Validate the database option."""
    valid_options = ["sqlalchemy_orm", "sqlalchemy_queries", "sqlmodel", "beanie", "none"]
    if db_option not in valid_options:
        message = f"ERROR: The database option `{db_option}` is not valid. Choose from {', '.join(valid_options)}."
        raise ValueError(message)


def validate_include_ml_exp_folder(include_ml_exp_folder: str) -> None:
    """Validate the include_ml_exp_folder option."""
    if include_ml_exp_folder not in ["y", "n"]:
        message = f"ERROR: The include_ml_exp_folder option `{include_ml_exp_folder}` is not valid. Choose either 'y' or 'n'."
        raise ValueError(message)


def main() -> None:
    try:
        validate_package_name(package_name=PACKAGE_NAME)
        validate_python_version(python_version=PYTHON_VERSION)
        validate_project_type(project_type=PROJECT_TYPE)
        validate_db_option(db_option=DB_OPTION)
        validate_include_ml_exp_folder(include_ml_exp_folder=INCLUDE_ML_EXP_FOLDER)
    except ValueError as ex:
        print(ex)
        sys.exit(1)


if __name__ == "__main__":
    main()
