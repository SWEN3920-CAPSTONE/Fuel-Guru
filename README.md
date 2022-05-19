# Fuel-Guru

This project is using pipenv for package management

## Setup Prerequisites

- PostreSQL is installed and database and user have been created
- .env file in project root with all variables having values

## Setup Instructions

Install pipenv (if not already installed)

```shell
pip install --user pipenv
```

Install all dependencies

```shell
pipenv install
```

Activate virtualenv (to run python commands)

```shell
pipenv shell
```

(pipenv doesn't require you to create a venv nor use and update a requirements.txt file)

Apply database migrations

```shell
flask db upgrade
```

### Additional Commands

To add a dependency

```shell
pipenv install <packagename>
```

To remove a dependency

```shell
pipenv uninstall <packagename>
```

To migrate the database after changes to the models (pipenv shell activated)

```shell
flask db migrate -m 'Description'
flask db upgrade
```

To run the server (pipenv shell activated)

```shell
python server.py
```

To add random test data to the database (pipenv shell activated)

```shell
python seed.py 
```
