"""This module is called after project is created."""
import textwrap
from pathlib import Path
import shutil
from typing import List

# Project root directory
PROJECT_DIRECTORY = Path.cwd().absolute()
PROJECT_NAME = "{{ cookiecutter.project_name }}"
GIT_REPO_URL = "{{ cookiecutter.git_repo_url }}"
GIT_PLATFORM = "{{ cookiecutter.ci_git_platform }}"
DB_OPTION = "{{ cookiecutter.db_option }}"
INCLUDE_ML_EXP_FOLDER = "{{ cookiecutter.include_ml_exp_folder }}" == "y"
PROJECT_TYPE = "{{ cookiecutter.project_type }}"


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


def remove_file(path: Path) -> None:
    """Remove a file if it exists."""
    path.unlink(missing_ok=True)


def remove_directory(path: Path) -> None:
    """Remove a directory and its contents if it exists."""
    shutil.rmtree(path, ignore_errors=True)


def move_file(src: Path, dst: Path) -> None:
    """Move a file from src to dst, creating parent directories if needed."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dst))


def remove_unrelated_ci_configuration(project_directory: Path, git_platform: str) -> None:
    """Remove CI configuration files not related to the chosen git platform."""
    if git_platform == "github":
        remove_file(project_directory / ".gitlab-ci.yml")
    elif git_platform == "gitlab":
        remove_directory(project_directory / ".github")
    elif git_platform == "none":
        remove_file(project_directory / ".gitlab-ci.yml")
        remove_directory(project_directory / ".github")
    else:
        raise ValueError(f"Unsupported git platform: {git_platform}")


def process_project_type(project_directory: Path, project_type: str) -> None:
    """Process project files based on the chosen project type."""
    app_dir = project_directory / "app"
    run_py = project_directory / "run.py"

    if project_type == "empty":
        # Remove all contents of app directory
        remove_directory(app_dir)
        # Recreate empty app directory
        app_dir.mkdir(exist_ok=True)
        # Move run.py into app directory
        if run_py.exists():
            shutil.move(str(run_py), str(app_dir / "run.py"))
        else:
            raise FileNotFoundError("run.py not found in project root")
        # Create empty __init__.py in app directory
        (app_dir / "__init__.py").touch()
    elif project_type == "fastapi_app":
        # Remove run.py for FastAPI projects
        remove_file(run_py)
    else:
        raise ValueError(f"Unsupported project type: {project_type}")
    # For "fastapi_app", we keep the existing structure


def process_db_files(project_directory: Path, db_option: str) -> None:
    """Process database-related files based on the chosen DB option."""
    app_dir = project_directory / "app"
    db_dirs = [app_dir / dir_name for dir_name in ["db", "models", "repositories"]]

    if db_option == "none":
        for dir_path in db_dirs:
            remove_directory(dir_path)
        return

    if db_option == "sqlalchemy_orm":
        process_sqlalchemy_orm(project_directory, app_dir)
    elif db_option == "sqlalchemy_queries":
        process_sqlalchemy_queries(project_directory, app_dir)
    elif db_option in ["sqlmodel", "beanie"]:
        process_other_db_option(app_dir, db_option)

    remove_empty_directories(db_dirs)

    if db_option != "sqlalchemy_orm":
        remove_file(project_directory / "alembic.ini")


def process_sqlalchemy_orm(project_directory: Path, app_dir: Path) -> None:
    """Process files for sqlalchemy_orm option."""
    db_dir = app_dir / "db" / "sqlalchemy"
    models_dir = app_dir / "models" / "sqlalchemy"
    repo_dir = app_dir / "repositories" / "sqlalchemy"

    # Move necessary files and directories
    for dir_path in [db_dir, models_dir, repo_dir]:
        if dir_path.exists():
            move_directory_contents(dir_path, dir_path.parent)
        dir_path.parent.parent.joinpath(dir_path.name).rmdir()

    # Remove queries.py
    remove_file(app_dir / "db" / "queries.py")

    # Process Alembic files
    process_alembic_files(project_directory)


def process_sqlalchemy_queries(project_directory: Path, app_dir: Path) -> None:
    """Process files for sqlalchemy_queries option."""
    db_dir = app_dir / "db" / "sqlalchemy"

    # Keep only session.py and queries.py
    if db_dir.exists():
        for item in db_dir.iterdir():
            if item.name not in ["session.py", "queries.py"]:
                remove_file(item) if item.is_file() else remove_directory(item)
        move_directory_contents(db_dir, db_dir.parent)
    db_dir.parent.parent.joinpath(db_dir.name).rmdir()

    # Remove models and repositories
    remove_directory(app_dir / "models")
    remove_directory(app_dir / "repositories")


def process_other_db_option(app_dir: Path, db_option: str) -> None:
    """Process files for sqlmodel or beanie options."""
    for dir_name in ["db", "models", "repositories"]:
        dir_path = app_dir / dir_name / db_option
        if dir_path.exists():
            move_directory_contents(dir_path, dir_path.parent)
        dir_path.parent.parent.joinpath(dir_path.name).rmdir()


def move_directory_contents(src_dir: Path, dst_dir: Path) -> None:
    """Move contents of src_dir to dst_dir and remove src_dir."""
    for item in src_dir.iterdir():
        shutil.move(str(item), str(dst_dir))
    src_dir.rmdir()


def process_alembic_files(project_directory: Path) -> None:
    """Process Alembic-related files."""
    db_dir = project_directory / "app" / "db"
    alembic_ini = db_dir / "migrations" / "alembic.ini"
    migrations_dir = db_dir / "migrations"

    if alembic_ini.exists():
        move_file(alembic_ini, project_directory / "alembic.ini")
    if migrations_dir.exists():
        shutil.move(str(migrations_dir), str(project_directory / "migrations"))


def remove_empty_directories(directories: List[Path]) -> None:
    """Remove directories if they are empty."""
    for dir_path in directories:
        if dir_path.exists() and not any(dir_path.iterdir()):
            dir_path.rmdir()


def process_ml_folder(project_directory: Path, include_ml_exp_folder: bool) -> None:
    """Process ML folder based on the include_ml_exp_folder parameter."""
    ml_dir = project_directory / "ml"
    if not include_ml_exp_folder and ml_dir.exists():
        remove_directory(ml_dir)


def main() -> None:
    """Main function to orchestrate the post-generation process."""
    print_further_instructions(project_name=PROJECT_NAME, git_repo_url=GIT_REPO_URL)
    process_project_type(PROJECT_DIRECTORY, PROJECT_TYPE)
    remove_unrelated_ci_configuration(PROJECT_DIRECTORY, GIT_PLATFORM)
    if PROJECT_TYPE == "fastapi_app":
        process_db_files(PROJECT_DIRECTORY, DB_OPTION)
    process_ml_folder(PROJECT_DIRECTORY, INCLUDE_ML_EXP_FOLDER)


if __name__ == "__main__":
    main()