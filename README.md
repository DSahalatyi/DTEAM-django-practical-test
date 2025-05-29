# DTEAM - Django Developer Practical Test
Welcome! This test will help us see how you structure a Django project, work with various tools, and handle common
tasks in web development. Follow the instructions step by step. Good luck!

## Requirements:
Follow PEP 8 and other style guidelines, use clear and concise commit messages and docstrings where needed, structure
your project for readability and maintainability, optimize database access using Django’s built-in methods, and provide
enough details in your README.

### Version Control System

1. Create a **public GitHub repository** for this practical test, for example: `DTEAM-django-
practical-test`.
2. Put the text of this test (all instructions) into `README.md`.
3. For each task, create a separate branch (for example, `tasks/task-1`, `tasks/task-2`, etc.).
4. When you finish each task, **merge** that branch back into main but **do not delete** the original task branch.

### Python Virtual Environment

1. Use **pyenv** to manage the Python version. Create a file named `.python-version` in your repository to store 
the exact Python version.
2. Use **Poetry** to manage and store project dependencies. This will create a `pyproject.toml` file.
3. Update your `README.md` with clear instructions on how to set up and use pyenv and Poetry for this project.


### Installation
**Install python using pyenv** ([Linux/MacOS](https://github.com/pyenv/pyenv)|[Windows](https://github.com/pyenv-win/pyenv-win))
```bash
pyenv install 3.12.8
pyenv local 3.12.8
```
**Install dependencies with [poetry](https://python-poetry.org/docs/)**
```bash
poetry install --no-root
```

Apply migrations & populate DB with test data
```bash
poetry run python manage.py migrate
poetry run python manage.py loaddata initial_data.json
```

### Run with Docker
**Configure `.env` file according to `.env.example`**
```shell
docker-compose build
docker-compose up
```