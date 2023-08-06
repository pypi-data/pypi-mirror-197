
# greeting_package

[![PyPI version](https://badge.fury.io/py/greeting-package.svg)](https://badge.fury.io/py/greeting-package)

`greeting-package` is a Python package for greeting people.

## Installation

You can install `greeting-package` via `pip`:

```bash
pip install greeting-package
```
## Usage
```
from greeting_package.greeting import say_hello

say_hello('John')  # 'Hello, John!'
say_hello('Jane')  # 'Hello, Jane!'
```
## Contributing

Bug reports and pull requests are welcome on GitHub at 
[Here](https://github.com/osundwajeff/greeting_package).

## Documentation

The greeting-package documentation includes:
- Installation instructions
- Usage examples
- API reference
- Development instructions

### API Reference
```
greeting_package.greeting.say_hello(name: str) -> str
```
Greet someone by name.
```
Parameters:

    name (str): # The name of the person to greet.

Returns:

    A greeting message (str).
```
## Contributing
Bug Reports and Feature Requests

Please use the issue tracker to report any bugs or feature requests.
Development

Clone the repository:
```
git clone https://github.com/osundwajeff/greeting_package.git
cd greeting-package
```
  Create a virtual environment:
```
python3 -m venv env
source env/bin/activate
```

Install development dependencies:
```
pip install -r requirements-dev.txt
```

Make changes and add tests.
Run the tests:
```
pytest tests/
```

Build the package:
```
python3 -m build
```

Install the package:
```
pip install .
```

Push your changes and create a pull request.

## License

greeting-package is released under the MIT License. See LICENSE for details.

