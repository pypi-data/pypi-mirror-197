# egnar
Python range-like iterator for float, decimal.Decimal and fractions.Fraction

```python
from egnar import *

for i in frange(0, 1, 0.1):
    print(i)

for i in drange(0, 1, '0.1'):
    print(i)

for i in farange(0, 1, '1/3'):
    print(i)
```