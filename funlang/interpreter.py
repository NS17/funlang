import re

from .parser import BinOp, UnaryOp, Constant, General, Expression, Conditional, Main, FunctionCall, AST
from .errors import InterpreterError


def camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


class Interpreter:
    """
    This class contains methods to execute AST structure returned by parser
    """
    def __init__(self):
        self.decs = []
        self.funcs = {}

    def execute(self, node: AST):
        method_name = 'execute_' + camel_to_snake(type(node).__name__)
        return getattr(self, method_name)(node)

    def execute_main(self, node: Main):
        # read functions definitions
        for fun in node.functions:
            if fun.name in self.funcs:
                raise InterpreterError(f'Repeated declaration {fun.name}')
            self.funcs[fun.name] = fun
        return self.execute_expression(node.expression)

    def execute_expression(self, node: Expression):
        decs = {}
        # store declarations
        for dec in node.declarations:
            name = dec.letter.value.value
            if name in decs:
                raise InterpreterError(f'Repeated declaration {name}')
            decs[name] = dec.declaration, False

        # add a scope
        self.decs.append(decs)

        result = self.execute(node.expression)
        self.decs.pop()
        return result

    def execute_bin_op(self, node: BinOp):
        return node.op.value[1](self.execute(node.left), self.execute(node.right))

    def execute_unary_op(self, node: UnaryOp):
        return node.op.value[2](self.execute(node.argument))

    def execute_constant(self, node: Constant):
        return float(node.value.value)

    def execute_general(self, node: General):
        for dec in self.decs[::-1]:
            if node.value.value in dec:
                if not dec[node.value.value][1]:
                    dec[node.value.value] = self.execute(dec[node.value.value][0]), True

                return dec[node.value.value][0]

        raise InterpreterError(f'Unknown variable {node.value.value}')

    def execute_conditional(self, node: Conditional):
        condition = self.execute(node.if_condition)
        if condition > 0:
            return self.execute(node.if_expression)
        return self.execute(node.else_expression)

    def execute_function_call(self, node: FunctionCall):
        if node.name not in self.funcs:
            raise InterpreterError(f'Unknown function {node.name}')
        function = self.funcs[node.name]

        args = {key.value.value: (self.execute(value), True) for key, value in zip(function.args, node.args)}
        self.decs.append(args)
        result = self.execute(function.body)
        self.decs.pop()
        return result
