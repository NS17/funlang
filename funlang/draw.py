from dataclasses import fields
from anytree import Node, RenderTree

from .parser import AST


def visualize(root):
    """
    Renders AST structure (after parsing) in root
    For example draws "x + y | x = 1 | y = 0" as
    Main
    └── Expression
        ├── BinOp
        │   ├── General
        │   └── General
        ├── Declaration
        │   ├── General
        │   └── Expression
        │       └── Constant
        └── Declaration
            ├── General
            └── Expression
                └── Constant
    :param root: AST
    :return: None
    """
    def convert(node: AST):
        children = []
        for x in fields(node):
            attr = getattr(node, x.name)
            if isinstance(attr, AST):
                children.append(attr)
            if isinstance(attr, (list, tuple)) and all(isinstance(x, AST) for x in attr):
                children.extend(attr)

        return Node(type(node).__name__, original=node, children=list(map(convert, children)))

    for pre, fill, node in RenderTree(convert(root)):
        print("%s%s" % (pre, node.name))
