try:
    # python >= 3.11
    # https://docs.python.org/3/library/tomllib.html
    import tomllib # type: ignore
except ImportError:
    # backport for python >= 3.7
    # https://realpython.com/python-toml/#load-toml-with-python
    import tomli as tomllib

tomllib = tomllib
