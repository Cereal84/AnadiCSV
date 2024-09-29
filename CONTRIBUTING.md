# Contributing

Please make sure to to the following guidelines to the best.

## Code quality

Due I'm a 'dirty' developer in order to force me to have at least some code quality standard I
rely on different tools.

All the following tools are visible in `pyproject.toml` file. 

### Formatting

__Tool:__ black
__Configuration:__ default settings.

```console
$ poetry run black anadi/

All done! ✨ 🍰 ✨
XX files left unchanged.
```

### Format import order

We use isort in order to fix import order and its format.

__Tool:__ isort
__Configuration:__ default settings.

```console
$ poetry run isort anadi/
```


### Linting

TODO

__Tool:__ ruff
__Configuration:__ details in `pyproject.toml` file.


### Typechecking

TODO

__Tool:__ mypy
__Configuration:__ default settings.

### Pre-commit

TODO

### Tests

Even if there is no test at all I prefer to use `pytest` for testing.

