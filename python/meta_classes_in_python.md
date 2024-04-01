# Metaclasses in python

You must have heard everything in python is an object. I did too. But the first
time I learnt classes were objects as well, it caught me by surprise. 
Classes are objects of `type`, which makes sense, as classes, int, strings,
tuples can all be lumped together as types. And I guess python wouldn't be python if
we didn't have a way to modify everything at runtime. You shouldn't
be surprised to learn that there is also way to change how classes are constructed
as well.

In this blog, we are going to learn how metaclasses can help you change how you
classes are constructed. I think the best way to learn about something in
programming is to learn what you can do with it. And we are going to do just
that by learning how to create metaclasses and what magic methods metaclasses offer.

## Base setup

```python
class Metaclass(type):
    pass

class Person(metaclass=Metaclass):
    pass
```

## Major methods
1. __new__ posibilities
```python
class Metaclass(type):
    def __new__(mcs, name, bases, namespace, **kwargs):
        return super().__new__(mcs, name, bases, namespace)
```


2. __prepare__ posibilities
```python
class Metaclass(type):
    def __prepare__(mcs, name, bases, namespace, **kwargs):
        return super().__new__(mcs, name, bases, namespace, **kwargs)
```

3. __call__ posibilities
```python
class Metaclass(type):
    def __class__(cls, *args, **kwargs):
        return super().__new__(mcs, name, bases, namespace, **kwargs)
```

4. custom methods.
Like any methods, in the class can be used by the instances of that class. Any
method you add to your metaclass can be accessed by the class (metainstance).
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
    Human.make() # This worlds and returns a Human object
```

Usecases:
Usually, it's best not to touch the metaclasses. It is seldom used in the application, for that
specific reason. Because they are powerful and thus, can be misused. You can return random
instances of random classes, add random variables and features to the classes, etc. But here
are some use cases nonetheless.

# TODO: READ and edit the following. Add code examples if possible.
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
