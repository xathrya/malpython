# Malicious Package

This package is used to demonstrate common tricks by threat actor to masquerade malicious code.

## Malicious Entry Points

Entry Point is mechanism to register a function, commonly used for:
- plugin hooks (e.g. `pytest11` for pytest plugins)
- cli tools (e.g. `console_script`)
- expose integrations to other tools (e.g. `mkdocs.plugins`, `tox`, etc).

Entry points are declared in `setup.py` or `pyproject.toml` and loaded automatically by the consuming tools.

This sample demonstrate how we add plugin for `pytest` and will be run everytome `pytest` is executed.

Because of this mechanism, our payload is passive and depends on the external event, making it more stealthy.

## Usage

To test locally, use following command for building and installing

```sh
# build
python3 -m build

# install
pip3 install dist/malpkg5-0.1.0.tar.gz
```

In this scenario, we are hooking into pytest. So, to trigger it we use to run pytest in any directory.

```sh
cd ~
pytest .
```

## Remarks

Some auto-triggered entry points for passive execution, implicitly import or run our module.

| Tool / Framework | Entry Point Group                    | When Triggered                              |
| ---------------- | ------------------------------------ | ------------------------------------------- |
| pytest     | `pytest11`                           | Automatically loads plugins on `pytest` run |
| mkdocs     | `mkdocs.plugins`                     | On build/serve                              |
| tox        | `tox`                                | On `tox` run                                |
| sphinx     | `sphinx.builders` / `sphinx.parsers` | On docs build                               |
| jupyter    | `jupyter_serverproxy_servers`        | On Jupyter startup                          |
| pylint     | `pylint.reporters`, `pylint.plugins` | On analysis                                 |
| black      | `black.plugins`                      | (optional) when used in some integrations   |
| setuptools | `distutils.commands`                 | On `python setup.py install`                |

Tools like those typically use `pkg_resources` or `importlib.metadata` like this to automatically load plugins

```python
for ep in pkg_resources.iter_entry_points("pytest11"):
    plugin = ep.load()      # our entry points run here
```

which will trigger load to the module.

