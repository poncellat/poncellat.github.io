Title: Python Common Gotchas
Date: 2022-09-04 09:31
Modified: 2022-09-04 09:31
Tags: python
Keywords: python,pythonprogramming,programming
Authors: Hephzibah Pon Cellat Arulprakash

This article discusses about common gotchas in python with code snippets describing what someone might think it would work like but how it actually works behind the scenes.

## Table of Contents

* Mutable Default Arguments
* Late Binding Closures
* List Copy
* Local Variable

## Mutable Default Arguments

```
def append_to(element, to=[]):
    to.append(element)
    return to

my_list = append_to(2)
print(my_list)

my_other_list = append_to(4)
print(my_other_list)
```

### What You Might Have Expected to Happen


A new list is created each time the function is called if a second argument isn’t provided, so that the output is:

```
[2]
[4]
```

### What actually happens


A new list is created once when the function is defined, and the same list is used in each successive call.
Python’s default arguments are evaluated once when the function is defined, not each time the function is called. This means that if you use a mutable default argument and mutate it, you will and have mutated that object for all future calls to the function as well.


```
[2]
[2, 4]
```

### What you should do instead


Create a new object each time the function is called, by using a default argument to signal that no argument was provided (None is often a good choice).

```
def append_to(element, to=None):

    if to is None:
        to = []

    to.append(element)
    return to
```

## Late Binding Closures

```
def create_multipliers():
    return [lambda x: i * x for i in range(5)]


for multiplier in create_multipliers():
    print(multiplier(2))
```

### What You Might Have Expected to Happen


A list containing five functions, That each have their own closed-over i variable that multiplies their argument, producing:

```
0
2
4
6
8
```

### What actually happens


Five functions are created but all of them just multiply x by 4.
Python’s closures are late binding. This means that the values of variables used in closures are looked up at the time the inner function is called.
Here, whenever any of the returned functions are called, the value of i is looked up in the surrounding scope at call time. By then, the loop has completed and i is left with its final value of 4.

```
8
8
8
8
8
```

### What you should do instead


You can create a closure that binds immediately to its arguments by using a default argument.

```
def create_multipliers():

    return [lambda x, i=i : i * x for i in range(5)]
```

## List Copy

```
array1 = [1, 2, 3, 4, 5]

array2 = array1
array2[0] = 10

print(array1)
print(array2)
```

### What You Might Have Expected to Happen

* array1 has values 1, 2, 3, 4, 5
* array2 is created with same values as like array1
* array2 first element is modified to 10
* array1 values are not changed

```
[1, 2, 3, 4, 5]
[10, 2, 3, 4, 5]
```

### What actually happens


* Variables are simply names that refer to objects.
* Doing array2=array1 doesn’t create a copy of the list
* It creates a new variable array2 that refers to the same object array1 refers to.
* This means that there is only one object (the list), and both array1 and array2 refer to it.
* Lists are mutable, which means that you can change their content.

```
[10, 2, 3, 4, 5]
[10, 2, 3, 4, 5]
```

### What you should do instead


Create a another object with same values of array1 using list copy method or slicing or list method.

```
array2 = array1.copy()

# or

array2 = array1[:]

# or

array2 = list(array1)
```

## Local Variable

Consider the below two code snippets

```
x = 1

def foo():
    print(x)

foo()
```

```
x = 1

def foo():
    x += 1
    print(x)


foo()
```

### What You Might Have Expected to Happen


* First code snippet prints x value 10
* Second code snippet should be x = x+1 and print 11

```
snippet1: 10
snippet2: 11
```

### What actually happens

* When you make an assignment to a variable in a scope, that variable becomes local to that scope and shadows any similarly named variable in the outer scope.
* Since the first statement in foo assigns a new value to x, the compiler recognizes it as a local variable.
* Consequently when the next statement print(x) attempts to print the uninitialized local variable and an error results.

```
snippet1: 10
snippet2: UnboundLocalError: local variable 'x' referenced before assignment
```

### What you should do instead


Use the global keyword to access the outer scope variable.

```
x = 10

def foo():
    global x
    x += 1
    print(x)


foo()
```

## References

* [https://docs.python-guide.org/writing/gotchas/](https://docs.python-guide.org/writing/gotchas/)
* [https://docs.python.org/3/faq/programming.html#why-did-changing-list-y-also-change-list-x](https://docs.python.org/3/faq/programming.html#why-did-changing-list-y-also-change-list-x)
* [https://stackoverflow.com/questions/2612802/how-do-i-clone-a-list-so-that-it-doesnt-change-unexpectedly-after-assignment](https://stackoverflow.com/questions/2612802/how-do-i-clone-a-list-so-that-it-doesnt-change-unexpectedly-after-assignment)
* [https://docs.python.org/3/faq/programming.html#why-am-i-getting-an-unboundlocalerror-when-the-variable-has-a-value](https://docs.python.org/3/faq/programming.html#why-am-i-getting-an-unboundlocalerror-when-the-variable-has-a-value)
* [https://realpython.com/python-scope-legb-rule/](https://realpython.com/python-scope-legb-rule/)