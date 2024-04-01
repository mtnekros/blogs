import types

type

class Tracing:
    count = 0 
    def __init__(self, name, bases, namespace):
        """Create a new class"""
        self.__name__ = name
        self.__bases__ = bases
        self.__namespace__ = namespace
        for name, value in namespace.items():
            object.__setattr__(self, name, value)
        Tracing.count += 1
        print(f"Tracing.count={Tracing.count}")

    def __call__(self, *args, **kwargs):
        """Create a new instance"""
        return Instance(self, *args, **kwargs)

class Instance:
    def __init__(self, klass, *args, **kwargs):
        self.attributes = set()
        self.initialized = False
        self.__klass__ = klass
        if "__init__" in self.__klass__.__namespace__:
            self.__klass__.__namespace__["__init__"](self, *args, **kwargs)
        self.initialized = True

    def __getattr__(self, name):
        try:
            value = self.__klass__.__namespace__[name]
        except KeyError:
            raise AttributeError(name)
        if type(value) is not types.FunctionType:
            return value
        return BoundMethod(value, self)

    def __setattr__(self, name, value):
        if name not in ("attributes", "initialized", "__klass__"):
            if not self.initialized:
                object.__setattr__(self, "attributes", self.attributes.union([name]))
            if self.initialized and name not in self.attributes and name not in self.__klass__.__namespace__:
                raise AttributeError(f"No such attribute: { name }")
        object.__setattr__(self, name, value)

class BoundMethod:
    def __init__(self, function, instance):
        self.function = function
        self.instance = instance

    def __call__(self, *args):
        print("calling", self.function, "for", self.instance, "with", args)
        return self.function(self.instance, *args)

class Trace(metaclass=Tracing):
    pass

class Person(Trace):
    n_updates = 0

    def __init__(self, name: str, age: int):
        print("Person.__init__ called")
        self.name = name
        self.age = age

    def show(self):
        print(f"Person(name={self.name}, age={self.age}, n_updates={Person.n_updates})")

    def make_older(self, yrs: int):
        self.age += yrs
        self.n_updates += 1

def test_tracer():
    person = Person("Diwash Tamang", 28)
    person.show()
    person.make_older(2)
    person.show()


if __name__ == "__main__":
    person = Person("Diwash Tamang", 28)
    person.show()
    person.make_older(2)
    person.show()
# p = Person("Diwash Tamang", 28)

# class Point:
#     x: int
#     y: int
#
# def attach_init(cls: type):
#     def init(self, x, y):
#         self.x = x
#         self.y = y
#     cls.__init__ = init
#     cls.__repr__ = lambda self: f"Point(x={self.x}, y={self.y})"
#
# attach_init(Point)
# print(Point(1, 3))
#
# class M(type):
#     def __new__(mcs, name, bases, namespace, **kwargs):
#         if "__repr__" not in namespace:
#             raise NotImplementedError("__repr__ has to be implemented in subclasses of this function")
#         return super(M, mcs).__new__(mcs, name, bases, namespace, **kwargs)
#
#     def __call__(cls, *args, **kwargs):
#         _obj = super(M, cls).__call__(*args, **kwargs)
#         print(f"From metaclass: {_obj}")
#         return _obj
#
# class A(metaclass=M):
#     x = None
#     y = None
#
#     def __new__(cls, *args, **kwargs):
#         _obj = super().__new__(cls)
#         print(_obj)
#         return _obj
#
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#
#     def __repr__(self):
#         return f"A(x={self.x}, y={self.y})"

# print(A(1, 2))
# print(A(2, 3))
# print(A(4, 5))

# TRYING SINGLETON WITH METACLASS
# class SingletonType(type):
#     def __new__(mcs, name, bases, namespace, **kwargs):
#         print(f"SingletonType.__new__: {name}")
#         namespace["initialized"] = False
#         def new(cls, *args, **kwargs):
#             if cls.initialized:
#                 raise Exception(f"{cls.__name__} already initialized!")
#             result = object().__new__(cls)
#             print(result)
#             return result
#         namespace["__new__"] = new
#         return super().__new__(mcs, name, bases, namespace, **kwargs)

# class Singleton(metaclass=SingletonType):
#     # def __new__(cls, *args, **kwargs):
#     #     print("Singleton.__new__")
#     #     return super().__new__(cls)
#     pass

# class Point(Singleton):
#     def __init__(self, x: str, y: str):
#         self.x = x
#         self.y = y

#     # def __new__(cls, *args, **kwargs):
#     #     print("Point.__new__")
#     #     return super().__new__(cls, *args, **kwargs)

#     def show(self):
#         print(f"Point(x={self.x}, y={self.y})")

# p1 = Point(1, 1)
# print(p1)

# # TRYING WITH METACLASS
# class SingletonType(type):
#     _instances = {}
#
#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             cls._instances[cls] = super().__call__(*args, **kwargs)
#         return cls._instances[cls]
#
# class Point(metaclass=SingletonType):
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#
#     def show(self):
#         print(f"Point(x={self.x}, y={self.y})")
#
# class Person(metaclass=SingletonType):
#     def __init__(self, name):
#         self.name = name
#
# Point(10, 10)
# p1 = Person("Diwash")
# print(p1.name)
# p2 = Person("Peter")
# print(p1.name, p2.name)
# print(f"{p1.name} is {p2.name} => {p1 is p2}")

# """ TRYING WITHOUT METACLASS """
# class SingletonError(Exception):
#     pass
#
# class Singleton:
#     _instance = None
#
#     def __new__(cls, *args, **kwargs):
#         print(f"{cls.__name__}: {args} {kwargs}")
#         if cls._instance:
#             raise SingletonError("Singleton Object Can't Be Created Twice")
#         cls._instance = super().__new__(cls)
#         return cls._instance
#
# class Point(Singleton):
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#
#     def show(self):
#         print(f"Point(x={self.x}, y={self.y})")
#
# class Person(Singleton):
#     def __init__(self, name):
#         self.name = name
#
# Point(10, 10)
# p1 = Person("Diwash")
# Singleton()
#
# print(Point._instance)
# print(Singleton._instance)
# print(Person._instance)
# # print(p1.name, p2.name)
# # print(f"{p1.name} is {p2.name} => {p1 is p2}")

# class UpperTuple(tuple):
#     def __new__(cls, iterable):
#         upper_iterable = (s.upper() for s in iterable)
#         return super().__new__(cls, upper_iterable)
#
# x = ("This", "is", "not", "that", "good")
# print(x)
# print(UpperTuple(x))
#
# object



""" TRY 1 """

# import copy
#
# def _make_init(annotations: dict):
#     init_str = (
#         f"def __init__(self, {','.join(annotations.keys())}):"
#         +
#         "".join(f"self.{_var} = {_var};" for _var in annotations.keys())
#     )
#     print(init_str)
#     return init_str
#
# def init(self, x, y):
#     self.x = x
#     self.y = y
#
#
# class DataClassMeta(type):
#     def __new__(mcs, name, bases, namespace, **kwargs):
#         annotations = namespace.get('__annotations__')
#         print(annotations)
#         # print(f"mcs: {mcs}")
#         # print(f"name: {name}")
#         # print(f"bases: {bases}")
#         # print(f"namespace: {namespace}")
#         # print(f"kwargs: {kwargs}")
#         return super().__new__(mcs, name, bases, namespace, **kwargs)
#
# class DataClass(metaclass=DataClassMeta):
#     pass
#
# class Point(DataClass):
#     x: int
#     y: int
#     # __instance: None = None
#
#     def __init__(self):
#         pass
#
#     def add(self, x, y):
#         self.x += x
#         self.y += y
#
#     def show(self):
#         print(f"Point(x={self.x}, y={self.y})")
#
# # x = Point()
# # x = Point()
# # x = Point(1, 2)
# # print(x.x, x.y)
#
# p = Point(1, 1)
# p.show()
# p.add(1, 1)
# p.show()
#
# my_dict = {}
# exec("x=1+1;y=0;p=Point(-1,-1);", globals(), locals())
# p.show()
# print(globals())
