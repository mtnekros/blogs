# Metaclasses in python

You must have heard everything in python is an object. I did too. But the first
time I learnt classes were objects as well, it caught me by surprise. 
Classes are objects of `type`, which makes sense, as classes, int, strings,
tuples can all be lumped together as types. And I guess python wouldn't be python if
we didn't have a way to modify everything at runtime. You shouldn't
be surprised to learn that there is also way to change how classes are constructed
as well. This is a way of metaprogramming. Metaprogramming is a programming
technique in which computer programs have the ability to treat other programs
as their data. It means that a program can be designed to read, generate,
analyze or transform other programs, and even modify itself while running.

In this blog, we are going to learn how metaclasses can help you change how you
classes are constructed. I think the best way to learn about something in
programming is to learn what you can do with it. And we are going to do just
that by learning how to create metaclasses and what magic methods metaclasses offer.

# TODO: add a few lines of metaprogramming

## Base setup

```python
# all metaclasses must inherit from type
class Metaclass(type):
    pass

class Person(metaclass=Metaclass):
    pass
```

## Major methods
1. __new__
Like the __new__ method of normal classes, __new__ is used for creating a new
instance. But in case of metaclasses, it returns a class. And it has different
parameters which are as follows:
mcs => 1st arguement is the metaclass itself.
name => name of the class
bases => tuple of base classes of the class
namespace => aka attrs is dictinoary that holds all the attributes,
methods, __annotations__, etc.

```python
class Metaclass(type):
    def __new__(mcs, name, bases, namespace, **kwargs):
        return super().__new__(mcs, name, bases, namespace)
```

Because we have access to all the methods and the instance variables of the class
in this function, we can use it do to many things.
1. Code generation
2. Type checking
3. Ensuring certain methods or variables are defined and many more.

# Example 1:
Here's a way to ensure all classes have __repr__ defined.

```python
class M(type):
    def __new__(mcs, name, bases, namespace, **kwargs):
        if "__repr__" not in namespace:
            raise NotImplementedError("__repr__ has to be implemented in subclasses of this function")
        return super(M, mcs).__new__(mcs, name, bases, namespace, **kwargs)

    def __call__(cls, *args, **kwargs):
        _obj = super(M, cls).__call__(*args, **kwargs)
        print(f"From metaclass: {_obj}")
        return _obj

class A(metaclass=M):
    x = None
    y = None

# This will raise an NotImplementedError
```

# Example 2:
A personal preference of mine is to use type annotations as much as possible in
python. So here's a way to ensures that parameterse of all the methods of
classes that inherit from `Base` have type annotations using metaclasses.

```python
import inspect
import types

class MetaClass(type):
    def __new__(mcs, name, bases, namespace, **kwargs):
        for attr, value in namespace.items():
            if type(value) is types.FunctionType:
                for param_key,param_val in inspect.signature(value).parameters.items():
                    if param_key not in ("self", "cls") and param_val.annotation == inspect._empty:
                        # raising exception
                        raise Exception(f"Class: {name} doesn't have annotations for method: {attr}")
        return super().__new__(mcs, name, bases, namespace)

class Base(metaclass=MetaClass)
    pass

class Fruit(Base):
    def __init__(self, name: str, price: float): This will pass the annotation check
        self.name = name
        self.price = price

    def get_price(self, count=1): # this will raise exception because count doesn't have type annotation
        return count * self.price

```
Error msg:
```
raise Exception(f"Class: {name} doesn't have annotations for method: {attr}")
Exception: Class: Fruit doesn't have annotations for method: get_price
```

Note: Although this is possible, it should be noted that this will slow down the code,
with all the type checking and calls to the inspect.signature.

#  Example 3: Code generation

```python
def _make_init(annotations: dict):
    return (
        f"def __init__(self, {','.join(annotations.keys())}):" +
        "".join(f"self.{_var} = {_var};" for _var in annotations.keys())
    )

class CodeGenerationMeta(type):
    def __new__(mcs, name, bases, namespace, **kwargs):
        annotations = namespace.get('__annotations__')
        _init = namespace.get('__init__')
        if annotations and not _init:
            # exec will execute the init str and add it to namespace
            exec(_make_init(annotations), globals(), namespace)
        return super().__new__(mcs, name, bases, namespace, **kwargs)

class DataClass(metaclass=DataClassMeta):
    pass

class Point(DataClass):
    x: int
    y: int

    def show(self):
        print(f"Point(x={self.x}, y={self.y})")

Point(1, 2) # works just fine!!! :D
```

2. __prepare__ posibilities
The __prepare__ method in Python metaclasses is a special method that allows
you to customize how the class namespace is prepared before the class body is
executed. This method is called before the class body is executed, and it must
return a mapping object (e.g., a dictionary-like object) that will be used as
the namespace for the class.

# Example 4: Adding class variables with __prepare__
```python
class NamespaceCustomizationType(type):
    @classmethod
    def __prepare__(mcs, name, bases):
        print(f"NamespaceCustomization.__prepare__ => mcs: {mcs} name: {name}: bases: {bases}")
        extra_attrs = super().__prepare__(mcs, name, bases)
        return {
            **extra_attrs,
            "_count": 0,
            "__repr__": lambda self: print("Fuck you")
        }

class Fruit(metaclass=NamespaceCustomizationType):
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

f = Fruit("Mango", 10)
print(f.name)
print(f.price)
print(f._count) # this is also here from the __prepare__ method
# note: f._count is a class variable not an instance variables. Unless you
# assign it value using the instance later in the code.;
```

3. __call__
This function is called when you create an instance using your class. When you
create an instance, Person(), you are basically calling the __call__ method of
your class Person. So meta-instance method of __call__ in a metaclass can
override that method.
```python
class Metaclass(type):
    def __call_(cls, *args, **kwargs):
        return cls(*args, **kwargs)
```
# Example 5: Creating singletons by overriding __call__ method
# TODO: Check this code once
```python
class SingletonType(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        print("In SingletonType().__call__")
        if cls not in cls._instances:
            cls._instances[cls] = cls(*args, **kwargs)
        return cls._instances[cls]

class Point(metaclass=SingletonType):
    def __init__(self):
        self.x = 10
        self.y = 20

    @classmethod
    def __call__(cls, *args, **kwargs):
        # not required but this is what happens when we create new instance
        print("In Point.__call__")
        self = super().__new__(cls)
        self.__init__(*args, **kwargs)
        return self

    def show(self):
        print(f"Point(x={self.x}, y={self.y})")

print(Point() is Point()) # will return true because they point to the same instance
```

4. custom methods.
Like any methods, in the class can be used by the instances of that class. Any
method you add to your metaclass can be accessed by the class (meta-instance).
And the instead of
```python
class Metaclass(type):
    def make(cls, *args, **kwargs):
        """
        Usually in a instance method of class, self or the instance gets passed
        by default as the first argument.  In the same way, in metaclasses,
        classes gets passed as the first argument to the instance method of a
        metaclass.  cls is like self here. (Classes are also called
        meta-instances.)
        """
        return cls(*args, **kwargs)

class Human(metaclass=Metaclass):
    pass

if __name__ == "__main__":
    Human.make() # This works and returns a Human object
```

Usecases:
Usually, it's best not to touch the metaclasses. It is seldom used in many
application, for that specific reason. Because they are powerful and thus, can
be misused. You can return random instances of random classes, add random
variables and features to the classes, etc. But here are some use cases
nonetheless.

# TODO: READ and edit the following and make it more readable
There are lots of things you could do with metaclasses. Most of these can also
be done with creative use of __getattr__, but metaclasses make it easier to
modify the attribute lookup behavior of classes. Here's a partial list.

* Enforce different inheritance semantics, e.g. automatically call base class
  methods when a derived class overrides
* Implement class methods (e.g. if the first argument is not named 'self')
* Implement that each instance is initialized with copies of all class
  variables
* Implement a different way to store instance variables (e.g. in a list kept
  outside the the instance but indexed by the instance's id())
* Automatically wrap or trap all or certain methods
* for tracing
* for precondition and postcondition checking
* for synchronized methods
* for automatic value caching
* When an attribute is a parameterless function, call it on reference (to mimic
  it being an instance variable); same on assignment
* Instrumentation: see how many times various attributes are used
* Different semantics for __setattr__ and __getattr__ (e.g. disable them when
  they are being used recursively)
* Abuse class syntax for other things
* Experiment with automatic type checking
* Delegation (or acquisition)
* Dynamic inheritance patterns
