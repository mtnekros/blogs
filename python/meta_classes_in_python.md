# Metaclasses in python

You must have heard everything in python is an object. I did too. But the first
time I learnt classes were objects as well, it caught me by surprise. Classes
are objects of `type`, which makes sense, as classes, int, strings, tuples can
all be lumped together as types. And I guess python wouldn't be python if we
didn't have a way to modify everything at runtime. Therefore, you shouldn't be
surprised to learn that there is also way to change how classes are
constructed. This is a also known as metaprogramming.

>> Metaprogramming is a programming technique in which computer programs have
>> the ability to treat other programs as their data. It means that a program can
>> be designed to read, generate, analyze or transform other programs, and even
>> modify itself while running.

You must have wondered how the models in Django Framework behave very
differently to normal classes. The fields are defined as class variables but
when you access it via an instance, it returns a value instead of the field.
And you can specify proxy models which works very different to normal models.
Django achieves this by making use of metaclasses and descriptors.

In this blog, we are going to learn how metaclasses can help you change how you
classes are constructed. I think the best way to learn programming is to write
code. So, i highly recommed you to take some of the examples here and add your
own tweaks to them. Let's get into how you can create metaclasses and what
magic methods metaclasses offer.

## Base setup
Metaclasses are created by inheriting from `type`. Here's a simple snippet
to show how they are created.

```python
# all metaclasses must inherit from type
class Metaclass(type):
    pass

class Person(metaclass=Metaclass):
    pass
```

## Methods in metaclasses
Now, let us get into some of the dunder method metaclasses offer And about what 
they can be used for.

1. __new__
Like the __new__ method of normal classes, __new__ is used for creating a new
instance. But in case of metaclasses, it returns a class. And it has different
parameters which are as follows:
    * mcs => 1st arguement is the metaclass itself.
    * name => name of the class
    * bases => tuple of base classes of the class
    * namespace => aka attrs is a dictinoary that holds all the attributes,
        methods, __annotations__, etc. that are defined within the body of the
        class.

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
4. When an attribute is a parameterless function, call it on reference (to mimic
  it being an instance variable); same on assignment
5. Implement that each instance is initialized with copies of all class
  variables

# Example 1: Enforcing methods/attributes in subclasses
Here's a simple example on how you can enforce 

```python
class M(type):
    def __new__(mcs, name, bases, namespace, **kwargs):
        # namespace contains all the attributes defined in the class including
        # variables, methods and module it was defined in.
        if "__repr__" not in namespace:
            raise NotImplementedError("__repr__ has to be implemented in subclasses of this function")
        return super(M, mcs).__new__(mcs, name, bases, namespace, **kwargs)


class Base(metaclass=M):
    pass

class Point(Base): # this will pass the check
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

class Line(Base): # this will raise an error because __repr__ is not defined in this class
    def __init__(self, points: list):
        self.points = points

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
with all the type checking and calls to the inspect.signature. Therefore I would not
recommend doing something like this in real applications.

#  Example 3: Code generation
Here is a way to generate an __init__ function based on the type annotations
provided in the class. We are also create instance variables from class
variables in this example.

```python
def _make_init(annotations: dict):
    """
    returns the __init__ function from the given annotations in string form
    """
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
    z: int = 10

    def show(self):
        print(f"Point(x={self.x}, y={self.y}, {self.z})")

Point(1, 2, 3) # works just fine!!! :D
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
            "swear": lambda self: print("Watch your profanity!")
        }

    # __call__ function is called when creating a cls instance
    def __call__(cls, *args, **kwargs):
        cls._count += 1
        return cls(*args, **kwargs)

class Fruit(metaclass=NamespaceCustomizationType):
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

f = Fruit("Mango", 10)
print(f.name)
print(f.price)
print(f._count) # this is also here from the __prepare__ method
print(f.swear())
# note: f._count is a class variable not an instance variables. Unless you
# assign it value using the instance later in the code.;
```

3. __call__
This function is called when you create an instance using your class. When you
create an instance, Person(), you are basically calling the __call__ method of
your class Person. And those are defined in your metaclasses.

```python
class Metaclass(type):
    def __call_(cls, *args, **kwargs):
        return cls(*args, **kwargs)
```
# Example 5: Creating singletons by overriding __call__ method

There are multiple ways to create the controversial singleton class. However,
you can override the __call__ method in your metaclass to achieve the same
result.

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

    def show(self):
        print(f"Point(x={self.x}, y={self.y})")

print(Point() is Point()) # will return true because they point to the same instance
```

# Example 6: Returning a potato object
As you can probably guess by now, with all the possiblities provided by the
metaclases, you can do some very stupid things. Such as returning a potato
instance everytime you create an object. And here's a way to do that.

```python
class Potato:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Hi there! My name is {self.name}"

class PotatoType(type):
    def __call__(cls, *args, **kwargs):
        return Potato("Brown Potato")

class Base(metaclass=PotatoType):
    pass

class Person(Base):
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Square(Base):
    def __init__(self, length):
        self.length = length

p = Person("Diwash", 24) # returns a potato object
s = Square(10) # returns a potato object
print(p)
print(s)
# Both will just print:
# Hi there! My name is Brown Potato.
```

4. custom methods.
Like any methods, in the class can be used by the instances of that class. Any
method you add to your metaclass can be accessed by the class (meta-instance).
And they are always going to be classmethods.

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

# Summary:
Metaclasses in Python often seem mysterious and esoteric to many developers,
but they are an incredibly powerful tool for metaprogramming. Hopefully, this
blog has demystified metaclasses by providing a comprehensive overview of what
they are, how they work, and why they are useful and about how it can produce
unpredictable behaviours.

However, it's important to consider whether using metaclasses is truly
necessary. While they offer powerful capabilities, the need to change class
behavior at this level may be minimal in many cases. Developers should
carefully evaluate whether metaclasses are the best solution for their specific
use case, or if there are alternative approaches that can achieve the desired
outcome more simply.

