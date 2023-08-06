# Pyleague

## Index

1. [Overview](#overview)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Tests](#tests)
6. [Deployment](#deployment)
   7.[Getting started:](#getting_started)

## <a name="overview">Overview</a>

Pyleague is a cli tool that helps organizing competitions.
After providing pyleague with a list of the competition's participants
you will be able to get the matches for each day of the competition.

## <a name="requirements">Requirements</a>

* System requirements

python >= 3.9

* Package requirements

Listed in pyproject.toml under '[tool.poetry.dependencies]'

## <a name="installation">Installation</a>

### For use

Fetch it from pip

```bash
pip install pyleague
```

### For development

To install package dependencies, install [poetry](https://python-poetry.org/docs/), then run the following command:

```bash
poetry install
```

## <a name="tests">Tests</a>

From root directory run:

~~~
pytest pyleague/tests
~~~

## <a name="deployment">Deployment</a>

Use poetry

```commandline
poetry build
```

```commandline
poetry publish
```

## <a name="getting_started">Getting started</a>

To try the app:

* Install it

* On your terminal run

```commandline
pyleague init
```

Define your league participants as asked.

* Check the matches for today

```commandline
pyleague today
```

* Update the league to the next day

```commandline
pyleague next
```

```commandline
pyleague today
```
