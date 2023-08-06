# Convigure

Easy configuration for Python with dot notation. Currently supports JSON and TOML.

## Installation
```
pip install convigure
```

## Usage
```python
from convigure import Conf

toml = Conf.load_toml("conf.toml")

print(toml.title)
print(toml.images[0])
```