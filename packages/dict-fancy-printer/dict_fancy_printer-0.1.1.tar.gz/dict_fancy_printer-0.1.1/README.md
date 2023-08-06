# dict-fancy-printer
A simple library used to print python dictionaries in a fancier and understandable way 


## Install

To install from pip:
```
pip install dict-fancy-printer
```

To install from master branch just do:
```
pip install git+https://github.com/matteogabburo/dict-fancy-printer
```

If you want to install a specific development branch, use
```
pip install git+https://github.com/matteogabburo/dict-fancy-printer@<branch_name>
```

## Usage

### FancyPrinter
- Example
```
from goburba.utils import FancyPrinter
printer = FancyPrinter()
print(printer(d))
```

### print_fancy_dict
- Example
```
from goburba.utils import print_fancy_dict
d = {"Hi": 1, "I":2, 3: "an", 4 : {"Matteo": 1, 2: "Gabburo"}}
print_fancy_dict(d)
```

### fancy_dict
- Example
```
from goburba.utils import fancy_dict
d = {"Hi": 1, "I":2, 3: "an", 4 : {"Matteo": 1, 2: "Gabburo"}}
d = fancy_dict(d)
print(d)
```