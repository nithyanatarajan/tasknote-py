# TaskNote
![CI](https://github.com/nithyanatarajan/tasknote-py/actions/workflows/ci.yml/badge.svg)

TaskNote is a personal productivity tool designed to manage notes and tasks with tags support. The tool also provides
insightful analytics about the user's daily activity and productivity trends.

## Installations

1. Install [uv](https://github.com/astral-sh/uv)

## Setup

### Virtual Environment Setup

```shell
uv venv
source .venv/bin/activate
```

### Install Dependencies

```shell
uv pip sync requirements.lock
```

## Running the Application

### Development mode (hot reload):

```bash
task run-dev
```

### Production mode:

```bash
task run
```

## Contribution

### Add a new dependency

```shell
uv pip install <package-name>
uv pip freeze > requirements.lock
```

### Update Dependencies

```shell
uv pip install --upgrade $(uv pip freeze | cut -d '=' -f1)
uv pip freeze > requirements.lock
```

### Format

```shell
task format
```

### Lint

```shell
task lint
```

### Running Tests

```bash
task test
```

### List All Tasks

```shell
task --list
```
