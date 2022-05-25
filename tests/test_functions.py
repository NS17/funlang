from funlang.utils import run_code


def test_fun():
    input_string = '''
    fun s(x, y):
      x + y + z
        | z = x * y
        || x = 2

    s(1, 1) + 2
    '''
    assert run_code(input_string) == 6

    input_string = '''
    fun incrsumpow(x, y, p):
        ((x + 1 if x < 0 else x + 2) + y) ** p
    
    t - incrsumpow(x, y, p) + 7 
        | t = 10
        | p = 4
        | x = 0
        | y = 1
    '''
    assert run_code(input_string) == -64
