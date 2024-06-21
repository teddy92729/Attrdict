# Attrdict

A simple way to access dictionary keys as attributes.

example:

```python-repl
from attrdict import AttrdictNone, AttrdictSymbol as Sym

example=dict(a=1,b=dict(c=2,d=3))

tmp=Sym.a.b @ example
if tmp is AttrdictNone:
	print("example has not key 'a.b'")
else:
	print(f"example has key 'a.b':{tmp}")

tmp=Sym.b.c @ example
if tmp is AttrdictNone:
	print("example has not key 'b.c'")
else:
	print(f"example has key 'b.c':{tmp}")
```
