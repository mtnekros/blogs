# ruff: noqa
# type: ignore

class SlottedPoint:

    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y

print(SlottedPoint.__dict__)

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(1, 2)
print(p.__dict__)

"""
By default, python looks for attributes in the __dict__ of the instance
* if it doesn't find it there, it will look for it in the __dict__ of the class
    * Slotted classes have descriptors for the attributes in the __dict__ 

{
    '__slots__': ('x', 'y'),
    'x': <member 'x' of 'SlottedPoint' objects>,
    'y': <member 'y' of 'SlottedPoint' objects>,
    '__doc__': None,
    ...
}

"""

class Member:
    def __get__(self, instance, owner):
        if owner is None:
            return self
        val = ... # C implementation to get the attribute from fixed offset
        return val

    def __set__(self, instance, owner):
        val = ...# C implementation to set the attribute from fixed offset

sp = SlottedPoint(1, 2)
print(Point.__dict__)
print(SlottedPoint.__dict__)
