from decimal import Decimal
from vtype import vnum, bidict
from vtype import vbool, vtrue, vfalse, uniset, empset, SysEmpty
from fractions import Fraction


# vbool
v1 = vbool(1)
v0 = vbool(0)
assert vbool is type(v1) is type(v0) is type(vtrue) is type(vfalse) is type(uniset) is type(empset) is type(SysEmpty)
assert v1 is vtrue
assert v0 is vfalse

# bidict
a = bidict()
a[1] = 10
assert a[1] == 10
assert a[10] == 1
assert a.pop(10) == 1
assert not a.core
assert a.get(5, 50) == 50
assert a.pop(6, 60) == 60

# # vnum
assert hash(3) == hash(3.0) == hash(Decimal('3')) == hash(Fraction(3)) == hash(vnum(3))
a = vnum(-1, 3)
b = vnum(10, -30)
c = vnum('-100', 300)
d = vnum(a)
e = vnum(a * 10, 10)
assert a == b == c == d == e
assert hash(a) == hash(b) == hash(c)
assert {3.0:1000}[3] == 1000
assert {3:1000}[3.0] == 1000
assert a * 10 == 10 * a
assert a + 10 == 10 + a
assert a - 10 + 10 == vnum(a)
assert 10 - a + a == vnum(10)
assert vnum(1) / 3 == vnum(1, 3)
assert 1 / vnum(3) == vnum(1, 3)
a = vnum(1)
d = {a:10000, 2:20000, 5:50000}
assert d[a] == d[1] == 10000
a += 1
assert d[a] == d[2] == 20000
a -= 1
assert d[a] == d[1] == 10000
a *= 5
assert d[a] == d[5] == 50000
a /= 5
assert d[a] == d[1] == 10000
a = vnum(1)
b = vnum(1)
assert id(a) != id(b)
a = vnum(3.5)
d = {a:100}
assert d[a] == d[3.5] == 100


print('测试通过')