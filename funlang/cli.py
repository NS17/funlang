import argparse

from funlang.utils import run_code


def entrypoint():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('filename', nargs='?', default=None, help='path to file containing code')
    group.add_argument('-c', help='string with code')

    args = parser.parse_args()
    if args.filename is not None:
        with open(args.filename, 'r') as f:
            input_string = f.read()
    else:
        input_string = args.c

    print(run_code(input_string))
