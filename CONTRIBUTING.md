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

__Tool:__ ruff
__Configuration:__ details in `pyproject.toml` file.

Check your code by calling:

```console
$ poetry run ruff anadi/

Poe => ruff check anadi
All checks passed!
```

If your code doesn't pass and you feel you have a good reason for it not to be, you may use
`noqa: ...` magic comments throughout the code, but please expect me to ask about it
when you submit the PR.

### Typechecking


__Tool:__ mypy
__Configuration:__ default settings.

```console
$ poetry run mypy anadi/

Success: no issues found in XX source files
```

### Pre-commit

I use `pre-commit` to run all the above checks before committing. You can install it by calling:

```console
$ poe pre-commit install
pre-commit installed at .git/hooks/pre-commit
```

### Tests

Even if there is no test at all I prefer to use `pytest` for testing.

