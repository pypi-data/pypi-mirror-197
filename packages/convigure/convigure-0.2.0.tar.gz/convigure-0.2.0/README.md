# Convigure

Easy configuration for Python with dot notation. Currently supports read-only JSON, YAML, and TOML.

## Installation

```
pip install convigure
```

## Usage

```python
from convigure import Conf

conf = Conf.load_toml("conf.toml")

# Or:
# conf = Conf.load_json("conf.json")

# Or:
# conf = Conf.load_yaml("conf.yaml")

print(conf.title)
print(conf.images[0])
```
