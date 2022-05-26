# Funlang

Funlang is a simple functional programming language implemented in Python.

## Installation

You can install it by

```shell
git clone https://github.com/NS17/funlang.git
cd funlang
pip install -e .
```

## Usage

You can execute code in funlang by running

```shell
funlang -c "code in funlang"
```

For example

```shell
funlang -c "x + y | x = 1 | y = 2"
```

Or using a file:

```shell
funlang filename.fun
```

## Syntax

Funlang can execute basic arithmetic operations like `+, -, *, /, **`. For example, you can run

```
5 * (9 + 7 - 8 / 4) ** (5 - 3)
```

It also supports variables with declarations through `|`. For example,

```
(x + y) ** 2 - t | x = 1 | y = 2 | t = 0
```

or in a more readable layout

```
(x + y) ** 2 - t 
  | x = 1 
  | y = 2 
  | t = 0
```

Declarations can be nested. So you can execute something like this:

```
(x + y) ** 2 - t 
    | x = 1
    | y = p ** r 
        || p = 9
        || r = x + 1
            ||| x = 8
    | t = 9 + r
        || r = 1
```

The number of `|` in declaration indicates the scope level.

Funlang also supports conditional statements and functions. For example:

```
fun incrsumpow(x, y, p):
    ((x + 1 if x < 0 else x + 2) + y) ** p

t - incrsumpow(x, y, p) + 7 
    | t = 10
    | p = 4
    | x = 0
    | y = 1
```

Outputs `-64.0`

## Tests

You can run tests via pytest

```shell
pytest tests
```
