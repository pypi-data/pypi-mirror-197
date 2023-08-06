# Offloading

[![PyPI - Version](https://img.shields.io/pypi/v/offloading.svg)](https://pypi.org/project/offloading)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/offloading.svg)](https://pypi.org/project/offloading)

Offloading tasks using processes

-----

**Table of Contents**

- [Installation](#installation)
- [License](#license)
- [Usage](#usage)

## Installation

```console
pip install offloading
```

## License

`offloading` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

## Usage

```python
from offloading import offload, Task


def get_result(x):
    return x * 2


future = Task.run(get_result, 2)
res = future.result(timeout=1)
assert res == 4


@offload
def heavy_processing(x):
    return x * 2


# blocking operation
res = heavy_processing(10)
assert res == 20
```

Check out `tests` for more.
