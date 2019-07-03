# Voices To Emotions Hackaton

## Design Guidelines

### Color Scheme

https://coolors.co/4495ff-7325f3-d81e5b-ea1a11-31a4a4

## coding Guidelines

We should use some conventions for the commit messages. We could use this one:

```
<type>(<scope>): <subject>
<BLANK LINE>
<body>
```

**Types** :

- **feat** : A new feature
- **fix** : A bug
- **chore** : A new recurent task
- **doc** : Documentation
- **refactor** : Code refactoring
- **init** : Project setup

**Scope** : Part of the project updated

**Subject** : What you did

**Body** : More detail description

## pipenv

In order to have the same environement, we will use [pipenv](https://github.com/pypa/pipenv). In order to install it _pip install pipenv_

Some useful commands:

- **pipenv install --dev** : Install all dependencies
- **pipenv install** _< nom package >_ : Installer a new dependence
- **pipenv run python** _< nom fichier.py >_ : Run a python file in the environment
