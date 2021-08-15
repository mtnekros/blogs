# What is Method Resolution Order (MRO) and how does it work in python?

## What kind of an order is the method resolution order?
It is the order in which the python searches for a method in a class heirarchy.
It is particularly useful when we are dealing with multiple inheritance. The
importance of method resolution isn't apparent until we are dealing with a
situation where we absolutely need it.

## Where is it required exactly?
Suppose we have the following situation. We have a father class and a mother
class. And we have a child class that inherits from both father and mother in
that order.
```python
class Father:
    def do_something(self):
        print("Called father's do_something")

class Mother: def do_something(self):
        print("Called mother's do_something")

class Child(Father, Mother):
    pass

child = Child()
child.do_something()
```
Which function will be called in this case when child.do_something() is called
since both the father and the mother have the function do_something? 
**This is exactly the type of situation where we need to linearlize the
order of classes in the heirarchy so that we can determine whose methods or
attribute takes precedence over the other.**

## How to get the mro of a class?
To display the method resolution order a class, we can either access the `__mro__`
attribute of the class or call the `Child.mro()` function. This will give
method resolution order. From which we can see that father's do_something method will
be called since it the first class in the mro that has do_something method.

```python
>>> Child.__mro__
(<class '__main__.Child'>, <class '__main__.Father'>, <class '__main__.Mother'>, <class 'o
bject'>)
>>> Child.mro()
[<class '__main__.Child'>, <class '__main__.Father'>, <class '__main__.Mother'>, <class 'o
bject'>]
```

## Simple trick to figure out the order in basic cases?
You can actually determine the mro in simple cases by just looking how it is
inherited using the **depth-first left-to-right scheme**.
+ First factor in the determining the precedence is depth of inheritance i.e.
  how far down the line the class is in the heirarchy. Lower the class higher
  it's precedence.
+ Another factor to consider is the position of the classes in the same
  generation and precedence goes from left to right. In our example `class
  Child(Father, Mother)`, Father classes comes before Mother.

## The actual algorithm used to determine MRO.
Although I said, you can use depth-first left-to-right scheme to determine mro in simple
cases, *for our ease*, the actual algorithm used for determination of MRO in python3 is
**C3 Linearization**. 
C3 linearization results in three important properties:
+ a consistent extended precedence graph
+ preservation of local precedence order
+ monotonic ordering

## C3 Linearization Description
+ <a name="c3l-def"> C3 linearization of a class is the sum of </a>
    + the class itself plus
    + a unique merge of
        + the linearizations of it's parents plus
        + the list of the parents.
+ The merge of the parent's linearization is done by selecting the first head
  of the list which doesn't appear in the tail of any other lists. The selected
  head is taken out of the merge list to the output list. 
+ The second step is repeated until all the classes are out of the merge list
  into the output list.

## Let's do a C3 serialization ourselves
```Python
# added the predefined base object class for the sake of simplication
class object:
    pass

class A(object):
    pass

class B(object):
    pass

class C(object):
    pass

class K(A, B, C):
    pass
```

First get the linearization of the base class.
```
L(object) = [object] <a name="eq1">--Eq1</a>// since it is has no base class it's linearization list only has itself
```

Now, to get the linearization of 1st generations.

From the definition of [C3 Linearization](#c3l-def)
```
L(A) = [A] + merge(L(object), [object]) 
     = [A] + merge([object], [object]) // from [Eq1](#eq1)
     = [A, object] // object added to the output list because it's the only head doesn't appear in any tail
```
Similarly, for B & C,
```
L(B) = [B, object] 
L(C) = [C, object]
```
Now, let's calculate the linearization for K

```
L(K) = [K] + merge(L(A), L(B), L(C), [A, B, C])                      // From the definition of [C3 Linearization](#c3l-def)
     = [K] + merge([A, object], [B, object], [C, object], [A, B, C]) // Replacing all the L(A), L(B), L(C) with their actual value
     = [K, A] + merge([object], [B, object], [C, object], [B, C])    // Added A to the output list because it only appears in the head of all list in the merge part
     = [K, A, B] + merge([object], [object], [C, object], [C])       // Skipped object (going from left to right) and added B to the output list because it only appears in the head of all list in the merge part
     = [K, A, B, C] + merge([object], [object], [object])
     = [K, A, B, C, object]
```

## Can you think of situation when multiple inheritance would break?
Since L3 linearization requires preservation of local precedence order. In the
following case, python won't let you do a multiple inheritance. 
```python
class A:
    pass

class B:
    pass

class M(A, B):
    pass

class N(B, A):
    pass

class X(M, N):
    pass
```

The order of A & B is reversed in M & N's inheritance. This doesn't
cause any problem. But when X inherits from both M and N, the local precedence
isn't preserved in the heirarchy of class X. Hence, that would fail with
the following error message.
```
TypeError: Cannot create a consistent method resolution
order (MRO) for bases A, B
```


## Conclusion
So, MRO is a pretty useful concept in python and any programming language that supports
multiple inheritance. It is the order in which python looks for method in a heirarchy of
classes. And in this blog, we learnt a bit about the inner workings of it. You can read
more about this topic in the links provided in the references section.

## References
[MRO by non other than Guido van Rossum himself](http://python-history.blogspot.com/2010/06/method-resolution-order.html)
