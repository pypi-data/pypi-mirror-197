# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring
# pylint: disable=locally-disabled, missing-function-docstring

import pytest

from illogical.evaluable import is_evaluable
from illogical.expression.comparison.eq import Eq
from illogical.expression.logical.and_exp import And
from illogical.illogical import Illogical
from illogical.operand.collection import Collection
from illogical.operand.reference import Reference, default_serialize_to
from illogical.operand.value import Value
from illogical.parser.parse import AND, DEFAULT_OPERATOR_MAPPING, EQ, Options


def mock_address(val: str) -> str:
    return default_serialize_to(val)


@pytest.mark.parametrize(
    "expression, expected",
    [
        (1, Value(1)),
        (mock_address("path"), Reference("path")),
        ([1], Collection([Value(1)])),
        ([DEFAULT_OPERATOR_MAPPING[EQ], 1, 1], Eq(Value(1), Value(1))),
        (
            [DEFAULT_OPERATOR_MAPPING[AND], True, True],
            And([Value(True), Value(True)]),
        ),
    ],
)
def test_parse(expression, expected):
    res = Illogical().parse(expression)
    assert is_evaluable(res) is True
    assert str(res) == str(expected)


@pytest.mark.parametrize(
    "expression, expected",
    [
        (1, 1),
        (mock_address("path"), "value"),
        ([1], [1]),
        ([DEFAULT_OPERATOR_MAPPING[EQ], 1, 1], True),
        ([DEFAULT_OPERATOR_MAPPING[AND], True, False], False),
    ],
)
def test_evaluate(expression, expected):
    assert Illogical().evaluate(expression, {"path": "value"}) == expected


@pytest.mark.parametrize(
    "expression, expected",
    [
        (1, 1),
        (mock_address("path"), "value"),
        (mock_address("nested.inner"), 2),
        (mock_address("list[1]"), 3),
        (mock_address("missing"), Reference("missing")),
        ([1], [1]),
        ([DEFAULT_OPERATOR_MAPPING[EQ], 1, 1], True),
        ([DEFAULT_OPERATOR_MAPPING[AND], True, True], True),
        (
            [DEFAULT_OPERATOR_MAPPING[AND], True, mock_address("missing")],
            Reference("missing"),
        ),
    ],
)
def test_simplify(expression, expected):
    res = Illogical().simplify(
        expression, {"path": "value", "nested": {"inner": 2}, "list": [1, 3]}
    )
    if is_evaluable(expected):
        assert str(res) == str(expected)
    else:
        assert res == expected


@pytest.mark.parametrize(
    "expression, expected",
    [
        (1, "1"),
        (True, "true"),
        ("val", '"val"'),
        ("$refA", "{refA}"),
        (["==", 1, 1], "(1 == 1)"),
        (["==", "$refA", "resolvedA"], '({refA} == "resolvedA")'),
        (["AND", ["==", 1, 1], ["!=", 2, 1]], "((1 == 1) AND (2 != 1))"),
    ],
)
def test_statement(expression, expected):
    assert Illogical().statement(expression) == expected


@pytest.mark.parametrize(
    "expression, expected",
    [
        (["IS", 1, 1], True),
        (["IS", 1, 2], False),
    ],
)
def test_operator_mapping(expression, expected):
    operator_mapping = DEFAULT_OPERATOR_MAPPING.copy()
    operator_mapping[EQ] = "IS"
    assert (
        Illogical(Options(operator_mapping=operator_mapping)).evaluate(expression, {})
        == expected
    )


@pytest.mark.parametrize(
    "expression, expected",
    [
        (["*AND", 1, 1], Collection([Value("AND"), Value(1), Value(1)])),
    ],
)
def test_escape_character(expression, expected):
    assert str(Illogical(Options(escape_character="*")).parse(expression)) == str(
        expected
    )
