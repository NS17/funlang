from funlang.utils import run_code


def test_declarations():
    s = '''
        x ** y
          | x = 2
          | y = z + 12
          || z = 3
          | t = 4
        '''
    assert run_code(s) == 32768

    s = 'x ** y | x=2 | y= x + 11'
    assert run_code(s) == 8192

    s = '''
        y + 1 + t
            | x = 1
            | t = x + 1
            | y = z + 12
            || z = x + 2
            || x = 0
        '''
    assert run_code(s) == 17

