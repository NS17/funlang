from funlang.utils import run_code


def test_simple():
    for s in ['2 + 2',
              '1 - 2 + 3',
              '5*9/4 + 12**3',
              '6**0 + -6*5']:
        assert run_code(s) == eval(s)


def test_brackets():
    s = '(((8 - 9) ** (7))) - (5) * 9 + (0*(6+4) - (8 + 1))'
    assert run_code(s) == eval(s)


def test_pow():
    for s in ['1 ** 7', '2 ** (9 - 1)', '6 ** (-5)']:
        assert run_code(s) == eval(s)

