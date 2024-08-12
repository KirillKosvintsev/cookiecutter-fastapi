"""This module is called after project is created."""
import textwrap
from pathlib import Path
import shutil
from typing import List, Callable

# Project configuration
PROJECT_CONFIG = {
    "DIRECTORY": Path.cwd().absolute(),
    "NAME": "{{ cookiecutter.project_name }}",
    "GIT_REPO_URL": "{{ cookiecutter.git_repo_url }}",
    "GIT_PLATFORM": "{{ cookiecutter.ci_git_platform }}",
    "DB_OPTION": "{{ cookiecutter.db_option }}",
    "INCLUDE_ML_EXP_FOLDER": "{{ cookiecutter.include_ml_exp_folder }}" == "y",
    "TYPE": "{{ cookiecutter.project_type }}"
}


def print_further_instructions(project_name: str, git_repo_url: str) -> None:
    """Show user what to do next after project creation."""
    project_directory = project_name.lower().replace(" ", "-")
    message = f"""
    Your project {project_name} is created.

    1) Now you can start working on it:

        $ cd {project_directory} && git init

    2) If you don't have Poetry installed run:

        $ make poetry-download

    3) Initialize poetry and install pre-commit hooks:

        $ make install
        $ make pre-commit-install

    4) Run formatters, linters, and tests:

        $ make format lint test

    5) Upload initial code to GitHub:

        $ git add .
        $ git commit -m "Initial commit"
        $ git branch -M main
        $ git remote add origin {git_repo_url}.git
        $ git push -u origin main
    """
    print(textwrap.dedent(message))


def file_operation(operation: Callable) -> Callable:
    """Decorator for file operations with error handling."""

    def wrapper(path: Path, *args, **kwargs):
        try:
            return operation(path, *args, **kwargs)
        except Exception as e:
            print(f"Error during {operation.__name__} for {path}: {str(e)}")

    return wrapper


@file_operation
def remove_file(path: Path) -> None:
    """Remove a file if it exists."""
    path.unlink(missing_ok=True)


@file_operation
def remove_directory(path: Path) -> None:
    """Remove a directory and its contents if it exists."""
    shutil.rmtree(path, ignore_errors=True)


@file_operation
def move_file(src: Path, dst: Path) -> None:
    """Move a file from src to dst, creating parent directories if needed."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dst))


def remove_unrelated_ci_configuration(project_directory: Path,
                                      git_platform: str) -> None:
    """Remove CI configuration files not related to the chosen git platform."""
    ci_configs = {
        "github": [".gitlab-ci.yml"],
        "gitlab": [".github"],
        "none": [".github", ".gitlab-ci.yml"]
    }
    for config in ci_configs.get(git_platform, []):
        path = project_directory / config
        remove_directory(path) if path.is_dir() else remove_file(path)


def process_project_type(project_directory: Path, project_type: str) -> None:
    """Process project files based on the chosen project type."""
    app_dir = project_directory / "app"
    run_py = project_directory / "run.py"

    if project_type == "empty":
        remove_directory(app_dir)
        app_dir.mkdir(exist_ok=True)
        if run_py.exists():
            shutil.move(str(run_py), str(app_dir / "run.py"))
        else:
            raise FileNotFoundError("run.py not found in project root")
    elif project_type == "fastapi_app":
        remove_file(run_py)
    else:
        raise ValueError(f"Unsupported project type: {project_type}")


def process_db_files(project_directory: Path, db_option: str) -> None:
    """Process database-related files based on the chosen DB option."""
    app_dir = project_directory / "app"
    db_dirs = [app_dir / dir_name for dir_name in
               ["db", "models", "repositories"]]

    if db_option == "none":
        for dir_path in db_dirs:
            remove_directory(dir_path)
        return

    db_processors = {
        "sqlalchemy_orm": process_sqlalchemy_orm,
        "sqlalchemy_queries": process_sqlalchemy_queries,
        "sqlmodel": process_other_db_option,
        "beanie": process_other_db_option
    }

    if db_option in db_processors:
        db_processors[db_option](app_dir, db_option)

    # Remove empty directories after processing
    remove_empty_directories(db_dirs)

    if db_option != "sqlalchemy_orm":
        remove_file(project_directory / "alembic.ini")


def process_sqlalchemy_orm(app_dir: Path, db_option: str) -> None:
    """Process files for sqlalchemy_orm option."""
    db_option = "sqlalchemy"
    for dir_name in ["db", "models", "repositories"]:
        base_dir = app_dir / dir_name
        sqlalchemy_dir = base_dir / db_option

        if sqlalchemy_dir.exists():
            # Remove other DB option directories
            for item in base_dir.iterdir():
                if item.is_dir() and item.name != db_option:
                    remove_directory(item)

            # Move sqlalchemy files to parent directory
            for item in sqlalchemy_dir.iterdir():
                shutil.move(str(item), str(base_dir))

            # Remove the now empty sqlalchemy directory
            remove_directory(sqlalchemy_dir)

    # Remove queries.py if it exists
    remove_file(app_dir / "db" / "queries.py")

    # Process alembic.ini
    alembic_ini = app_dir / "db" / "alembic.ini"
    if alembic_ini.exists():
        move_file(alembic_ini, app_dir.parent / "alembic.ini")


def process_sqlalchemy_queries(app_dir: Path, db_option: str) -> None:
    """Process files for sqlalchemy_queries option."""
    db_option = "sqlalchemy"
    db_dir = app_dir / "db"
    sqlalchemy_dir = db_dir / db_option

    # Remove other DB directories
    for dir_name in ["models", "repositories"]:
        remove_directory(app_dir / dir_name)

    if sqlalchemy_dir.exists():
        # Remove other DB option directories
        for item in db_dir.iterdir():
            if item.is_dir() and item.name != db_option:
                remove_directory(item)

        # Keep only session.py and queries.py
        for item in sqlalchemy_dir.iterdir():
            if item.is_file() and item.name in ["session.py", "queries.py"]:
                shutil.move(str(item), str(db_dir))
            else:
                remove_file(item) if item.is_file() else remove_directory(item)

        # Remove the now empty sqlalchemy directory
        remove_directory(sqlalchemy_dir)


def process_other_db_option(app_dir: Path, db_option: str) -> None:
    """Process files for sqlmodel or beanie options."""
    for dir_name in ["db", "models", "repositories"]:
        base_dir = app_dir / dir_name
        option_dir = base_dir / db_option

        if option_dir.exists():
            # Remove other DB option directories
            for item in base_dir.iterdir():
                if item.is_dir() and item.name != db_option:
                    remove_directory(item)

            # Move files from db_option directory to parent
            for item in option_dir.iterdir():
                if item.is_file():
                    shutil.move(str(item), str(base_dir))

            # Remove the now empty db_option directory
            remove_directory(option_dir)


def remove_empty_directories(directories: List[Path]) -> None:
    """Remove directories if they are empty."""
    for dir_path in directories:
        if dir_path.exists() and not any(dir_path.iterdir()):
            dir_path.rmdir()


def process_ml_folder(project_directory: Path,
                      include_ml_exp_folder: bool) -> None:
    """Process ML folder based on the include_ml_exp_folder parameter."""
    ml_dir = project_directory / "ml"
    if not include_ml_exp_folder and ml_dir.exists():
        remove_directory(ml_dir)


def main() -> None:
    """Main function to orchestrate the post-generation process."""
    print_further_instructions(project_name=PROJECT_CONFIG["NAME"],
                               git_repo_url=PROJECT_CONFIG["GIT_REPO_URL"])
    process_project_type(PROJECT_CONFIG["DIRECTORY"], PROJECT_CONFIG["TYPE"])
    remove_unrelated_ci_configuration(PROJECT_CONFIG["DIRECTORY"],
                                      PROJECT_CONFIG["GIT_PLATFORM"])
    process_ml_folder(PROJECT_CONFIG["DIRECTORY"],
                      PROJECT_CONFIG["INCLUDE_ML_EXP_FOLDER"])
    if PROJECT_CONFIG["TYPE"] == "fastapi_app":
        process_db_files(PROJECT_CONFIG["DIRECTORY"],
                         PROJECT_CONFIG["DB_OPTION"])


if __name__ == "__main__":
    main()
