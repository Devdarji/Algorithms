# Bencode Parser

A minimal implementation of the Bencode encoding format used by BitTorrent.

## Files

- `parser.py` - Core parser implementation
- `examples.py` - Comprehensive examples and explanations
- `README.md` - This file

## Usage

```python
from parser import encode, decode

# Encode Python objects to bencode
data = {b'key': b'value', b'number': 42}
encoded = encode(data)

# Decode bencode to Python objects
decoded = decode(encoded)
```

## Supported Types

| Python Type | Bencode Format | Example |
|-------------|----------------|---------|
| `bytes` | `<length>:<string>` | `b'5:hello'` |
| `int` | `i<integer>e` | `b'i42e'` |
| `list` | `l<contents>e` | `b'l5:helloi42ee'` |
| `dict` | `d<contents>e` | `b'd3:keyi123ee'` |

## Run Examples

```bash
python examples.py
```

This will show encoding/decoding examples for all supported types, including a complete BitTorrent file structure.
