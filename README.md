# iturtle

[![Build Status](https://travis-ci.org/datarho.tech/iturtle.svg?branch=master)](https://travis-ci.org/datarho.tech/iturtle)
[![codecov](https://codecov.io/gh/datarho.tech/iturtle/branch/master/graph/badge.svg)](https://codecov.io/gh/datarho.tech/iturtle)

A Custom Jupyter Widget Library

## Installation

You can install using `pip`:

```bash
pip install iturtle
```

## Development Installation

Create a dev environment:

```bash
conda env create -f environment.yml
```

Install the python. This will also build the TS package.

```bash
pip install -e ".[test, examples]"
```

When developing your extensions, you need to manually enable your extensions with the
lab frontend. For lab, this is done by the command:

```
jupyter labextension develop --overwrite .
yarn run build
```

### How to see your changes

#### Typescript:

If you use JupyterLab to develop then you can watch the source directory and run JupyterLab at the same time in different
terminals to watch for changes in the extension's source and automatically rebuild the widget.

```bash
# Watch the source directory in one terminal, automatically rebuilding when needed
yarn run watch
# Run JupyterLab in another terminal
jupyter lab
```

After a change wait for the build to finish and then refresh your browser and the changes should take effect.

#### Python:

If you make a change to the python code then you will need to restart the notebook kernel to have it take effect.
