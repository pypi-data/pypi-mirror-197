"""
A micro conditional engine used to parse the logical and comparison expressions,
evaluate an expression in data context, and provide access to a text form of the
given expression.
"""

from illogical.evaluable import (
    Context,
    Evaluable,
    Evaluated,
    Expression,
    flatten_context,
)
from illogical.parser.parse import Options, parse


class Illogical:
    """
    Illogical conditional engine.
    """

    def __init__(self, options: Options = Options()) -> None:
        self.options = options

    def parse(self, expression: Expression) -> Evaluable:
        """
        Parse given expression into an Evaluable object., i.e. it returns the parsed
        self-evaluable condition expression.

        Example:

        evaluable = illogical.parse(["==", "$name", "peter"])

        evaluable.evaluate({ "name": "peter" })
            True

        str(evaluable)
            ({name} == "peter")
        """

        return parse(expression, self.options)

    def evaluate(self, expression: Expression, context: Context) -> Evaluated:
        """
        Evaluate expression in the given context.

        Example:

        context = { "name": "peter" }

        illogical.evaluate(["==", 5, 5], context)
            True

        illogical.evaluate(["AND", ["==", 5, 5], ["==", "$name", "john"]], context)
            False
        """

        return self.parse(expression).evaluate(flatten_context(context))

    def simplify(
        self, expression: Expression, context: Context
    ) -> Evaluated | Evaluable:
        """
        Simplify an expression in a given context. This is useful when you already
        have some of the properties of context and wants to try to evaluate the
        expression.

        Example:

        illogical.simplify(["AND", ["==", "$a", 10], ["==", "$b", 20]], { "a": 10 })
            ({b} == 20)

        illogical.simplify(["AND", ["==", "$a", 10], ["==", "$b", 20]], { "a": 20 })
            False
        """

        return self.parse(expression).simplify(flatten_context(context))

    def statement(self, expression: Expression) -> str:
        """
        Expression string representation.

        Example:

        illogical.statement(["==", 5, 5])
            (5 == 5)

        illogical.statement(["AND", ["==", 5, 5], ["==", 10, 10]])
            ((5 == 5) AND (10 == 10))
        """

        return str(self.parse(expression))
