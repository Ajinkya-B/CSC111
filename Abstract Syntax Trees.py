"""
This file goes over some of the methods we used to work with abstract syntax trees.

Copyright and Usage Information
===============================
This file is Copyright (c) 2021 Ajinkya Bhosale.
"""

from __future__ import annotations
from typing import Any, Union, Optional


class Statement:
    """An abstract class representing a Python statement.
    """
    def evaluate(self, env: dict[str, Any]) -> Optional[Any]:
        """Evaluate this statement with the given environment.
        """
        raise NotImplementedError


class Expr(Statement):
    """An abstract class representing a Python expression.
    """


################################################################################
# Arithmetic Expression
################################################################################
class Num(Expr):
    """A numeric literal.

    Instance Attributes:
        - n: the value of the literal
    """
    n: Union[int, float]

    def __init__(self, number: Union[int, float]) -> None:
        """Initialize a new numeric literal."""
        self.n = number

    def evaluate(self, env: dict[str, Any]) -> Any:
        """Return the *value* of this expression.

        The returned value should the result of how this expression would be
        evaluated by the Python interpreter.

        >>> expr = Num(10.5)
        >>> env = {}
        >>> expr.evaluate(env)
        10.5
        """
        return self.n  # Simply return the value itself!

    def __str__(self) -> str:
        """Return a string representation of this expression.

        One feature we'll stick with for all Expr subclasses here is that we'll
        want to return a string that is valid Python code representing the same
        expression.

        >>> str(Num(5))
        '5'
        """
        return str(self.n)


class BinOp(Expr):
    """An arithmetic binary operation.

    Instance Attributes:
        - left: the left operand
        - op: the name of the operator
        - right: the right operand

    Representation Invariants:
        - self.op in {'+', '*'}
    """
    left: Expr
    op: str
    right: Expr

    def __init__(self, left: Expr, op: str, right: Expr) -> None:
        """Initialize a new binary operation expression.

        Preconditions:
            - op in {'+', '*'}
        """
        self.left = left
        self.op = op
        self.right = right

    def evaluate(self, env: dict[str, Any]) -> Any:
        """Return the *value* of this expression.

        The returned value should the result of how this expression would be
        evaluated by the Python interpreter.

        >>> expr = BinOp(Num(10.5), '+', Num(30))
        >>> env = {}
        >>> expr.evaluate(env)
        40.5
        """
        left_val = self.left.evaluate(env)
        right_val = self.right.evaluate(env)

        if self.op == '+':
            return left_val + right_val
        elif self.op == '*':
            return left_val * right_val
        else:
            # We shouldn't reach this branch because of our representation invariant
            raise ValueError(f'Invalid operator {self.op}')

    def __str__(self) -> str:
        """Return a string representation of this expression.
        """
        return f'({str(self.left)} {self.op} {str(self.right)})'


################################################################################
# Boolean Expression
################################################################################
class Bool(Expr):
    """A boolean literal.

    Instance Attributes:
        - b: the value of the literal
    """
    b: bool

    def __init__(self, b: bool) -> None:
        """Initialize a new boolean literal."""
        self.b = b

    def evaluate(self, env: dict[str, Any]) -> Any:
        """Return the *value* of this expression.

        The returned value should the result of how this expression would be
        evaluated by the Python interpreter.

        >>> expr = Bool(True)
        >>> env = {}
        >>> expr.evaluate(env)
        True
        """
        return self.b

    def __str__(self) -> str:
        """Return a string representation of this expression.
        """
        return str(self.b)


class BoolOp(Expr):
    """A boolean operation.

    Represents either a sequence of `and`s or a sequence of `or`s.
    Unlike BinOp, this expression can contains more than two operands,
    each separated by SAME operator:

        True and False and True and False
        True or False or True or False

    Instance Attributes:
        - op: the name of the boolean operation
        - operands: a list of operands that the operation is applied to

    Representation Invariants:
        - self.op in {'and', 'or'}
        - len(self.operands) >= 2
        - every expression in self.operands evaluates to a boolean value
    """
    op: str
    operands: list[Expr]

    def __init__(self, op: str, operands: list[Expr]) -> None:
        """Initialize a new boolean operation expression.

        Preconditions:
            - op in {'and', 'or'}
            - len(operands) >= 2
            - every expression in operands evaluates to a boolean value
        """
        self.op = op
        self.operands = operands

    def evaluate(self, env: dict[str, Any]) -> Any:
        """Return the *value* of this expression.

        The returned value should the result of how this expression would be
        evaluated by the Python interpreter.

        >>> expr = BoolOp('and', [Bool(True), Bool(True), Bool(False)])
        >>> env = {}
        >>> expr.evaluate(env)
        False
        >>> expr = BoolOp('or', [Bool(True), Bool(False), Bool(True), Bool(False)])
        >>> expr.evaluate(env)
        True
        >>> expr = BoolOp('or', [Bool(False), Bool(False),\
        BoolOp('and', [Bool(True), Bool(True), Bool(True)]), Bool(False)])
        >>> expr.evaluate(env)
        True
        """
        first = self.operands[0].evaluate(env)
        rest = self.operands[1:]

        if self.op == 'or':
            if first:
                return True
            elif len(rest) == 1:
                return self.operands[1].evaluate(env)
            else:
                return BoolOp('or', rest).evaluate(env)
        elif self.op == 'and':
            if not first:
                return False
            elif len(rest) == 1:
                return self.operands[1].evaluate(env)
            else:
                return BoolOp('and', rest).evaluate(env)
        else:
            raise ValueError(f'Invalid operator {self.op}')

    def __str__(self) -> str:
        """Return a string representation of this boolean expression.

        >>> expr = BoolOp('and', [Bool(True), Bool(True), Bool(False)])
        >>> str(expr)
        '(True and True and False)'
        """
        op_string = f' {self.op} '
        return f'({op_string.join([str(v) for v in self.operands])})'


class Compare(Expr):
    """A sequence of comparison operations.

    In Python, it is possible to chain together comparison operations:
        x1 <= x2 < x3 <= x4

    This is logically equivalent to the more explicit binary form:
        (x1 <= x2) and (x2 <= x3) and (x3 <= x4),
    except each expression (x1, x2, x3, x4) is only evaluated once.

    Instance Attributes:
        - left: The leftmost value being compared. (In the example above, this is `x1`.)
        - comparisons: A list of tuples, where each tuple stores an operation and
            expression. (In the example above, this is [(<=, x2), (<, x3), (<= x4)].)

    Note: for the purpose of this prep, we'll only allow the comparison operators <= and <
    for this class (see representation invariant below).

    Representation Invariants:
        - len(self.comparisons) >= 1
        - all(comp[0] in {'<=', '<'} for comp in self.comparisons)
        - self.left and every expression in self.comparisons evaluate to a number value
    """
    left: Expr
    comparisons: list[tuple[str, Expr]]

    def __init__(self, left: Expr,
                 comparisons: list[tuple[str, Expr]]) -> None:
        """Initialize a new comparison expression.

        Preconditions:
            - len(comparisons) >= 1
            - all(comp[0] in {'<=', '<'} for comp in comparisons)
            - left and every expression in comparisons evaluate to a number value
        """
        self.left = left
        self.comparisons = comparisons

    def evaluate(self, env: dict[str, Any]) -> Any:
        """Return the *value* of this expression.

        The returned value should the result of how this expression would be
        evaluated by the Python interpreter.

        >>> expr = Compare(Num(1), [('<=', Num(1))])
        >>> env = {}
        >>> expr.evaluate(env)
        True
        >>> expr = Compare(Num(1), [
        ...            ('<=', Num(2)),
        ...            ('<', Num(4.5)),
        ...            ('<=', Num(4.5))])
        >>> expr.evaluate(env)
        True
        """
        first = self.left.evaluate(env)
        second = self.comparisons[0][1].evaluate(env)
        rest = self.comparisons

        if rest[0][0] == '<':
            if len(rest) == 1:
                return first < second
            elif first < second:
                return Compare(rest[0][1], rest[1:]).evaluate(env)
            else:
                return False
        elif rest[0][0] == '<=':
            if len(rest) == 1:
                return first <= second
            elif first <= second:
                return Compare(rest[0][1], rest[1:]).evaluate(env)
            else:
                return False
        else:
            raise ValueError(f'Invalid operator {rest[0][0]}')

    def __str__(self) -> str:
        """Return a string representation of this comparison expression.

        >>> expr = Compare(Num(1), [
        ...            ('<=', Num(2)),
        ...            ('<', Num(4.5)),
        ...            ('<=', Num(4.5))])
        >>> str(expr)
        '(1 <= 2 < 4.5 <= 4.5)'
        """
        s = str(self.left)
        for operator, subexpr in self.comparisons:
            s += f' {operator} {str(subexpr)}'
        return '(' + s + ')'


class Name(Expr):
    """A variable expression.

    Instance Attributes:
      - id: The variable name in this expression.
    """
    id: str

    def __init__(self, id_: str) -> None:
        """Initialize a new variable expression."""
        self.id = id_

    def evaluate(self, env: dict[str, Any]) -> Any:
        """Return the *value* of this expression using the given variable environment.
        """
        if self.id in env:
            return env[self.id]
        else:
            raise NameError


################################################################################
# Boolean Expression
################################################################################
class Assign(Statement):
    """An assignment statement (with a single target).

    Instance Attributes:
      - target: the variable name on the left-hand side of the = sign
      - value: the expression on the right-hand side of the = sign
    """
    target: str
    value: Expr

    def __init__(self, target: str, value: Expr) -> None:
        """Initialize a new Assign node."""
        self.target = target
        self.value = value

    def evaluate(self, env: dict[str, Any]) -> None:
        """Evaluate this statement.

        This does the following: evaluate the right-hand side expression,
        and then update <env> to store a binding between this statement's
        target and the corresponding value.

        >>> stmt = Assign('x', BinOp(Num(10), '+', Num(3)))
        >>> env = {}
        >>> stmt.evaluate(env)
        >>> env['x']
        13
        """
        env[self.target] = self.value.evaluate(env)
