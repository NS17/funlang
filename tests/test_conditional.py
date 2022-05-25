from funlang.utils import run_code


def test_conditional():
    s = '1 if x + y > 0 else 2 - x | x = 0 | y = 1'
    assert run_code(s) == 1

    s = '1 if x + y > 0 else 2 - x | x = 0 | y = -1'
    assert run_code(s) == 2

    s = '(1 if x + y > 0 else 2) - x * (0 if x - y > 0 else 8) | x = 1 | y = -1'
    assert run_code(s) == 2

    s = '(5 if t + 1 > 2 else 4) - ((0 if t > 0 else 1)*4) | t = 1'
    assert run_code(s) == 4

    s = '(5 if t + 1 > 2 else 4) - ((0 if t > 0 else 1)*4) | t = -1'
    assert run_code(s) == 0

    s = '(5 if t + 1 > 2 else 4) - ((0 if t > 0 else 1)**4) | t = -1'
    assert run_code(s) == 3

