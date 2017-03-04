# config

This package allows you to handle config file easily while allowing you to override settings through commandline params.


-----------------
## Overview
*config.cfg:*
```commandline
a = 1
b = 2.2
s = 'abc'
```
*python script `test.py`:*
```python
from config import config
config.add_argument("-c", type=str, default="test")
print(config.a)
print(config.b)
print(config.s)
print(config.c)
```

```commandline
python test.py -c def --a 2
```

Output:
```commandline
2
2.2
abc
def
```
The value of config.a is overrided to 2 (it's 1 be default) by commandline