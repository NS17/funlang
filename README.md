# Funlang

Funlang is a simple functional programming language implemented in Python.

## Installation

You can install package by

```commandline
git clone git@github.com:NS17/interpreter.git
pip install -e .
```

## Usage

You can execute code in funlang by running

```commandline
funlang -c "code in funlang"
```

For example

```commandline
funlang -c "x + y | x = 1| y = 2"
```

Or using a file:

```commandline
funlang filename.fun
```

## Syntax

Funlang can execute basic arithmetic operations like `+, -, *, /, **`.
For example, you can run

```commandline
5 * (9 + 7 - 8 / 4)**(5 - 3)
```

It also supports variables with declarations through `|`.
For example,

`(x + y) - t | x = 1 | y = 2 | t = 0`

Declarations can be nested. So you can execute something like this:

```
(x + y) - t 
    | x = 1
    | y = p ** r 
        || p = 9
        || r = x + 1
            ||| x = 8
    | t = 9 + r
        || r = 1
```

The number of `|` in declaration indicated the scope level.

Funlang also supports conditional statements and functions.
For example:

```
fun incr_sum_pow(x, y, p):
    x = x + 1 if x < 0 else x + 2
    (x + y) ** p
    
t - incr_sum_pow(x, y, p) + 7 
    | t = 10
    | p = 4
    | x = 0
    | y = 1
```