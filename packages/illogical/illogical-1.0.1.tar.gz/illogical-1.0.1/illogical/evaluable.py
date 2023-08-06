"""Evaluable expression."""

from __future__ import annotations

from typing import Any, Iterable, NewType, Protocol

Context = dict[str, Any]
Primitive = str | int | float | bool | None
Evaluated = Primitive | Iterable["Evaluated"]
Expression = Evaluated

Kind = NewType("Kind", str)


def is_primitive(subject) -> bool:
    """
    Is subject a primitive value predicate.
    """

    return subject is None or isinstance(subject, (str, int, float, bool))


def is_evaluable(subject) -> bool:
    """
    Is subject a evaluable object predicate.
    """

    return all(
        hasattr(subject, method) for method in ("evaluate", "serialize", "simplify")
    )


class Evaluable(Protocol):
    """Evaluable expression."""

    def evaluate(self, context: Context) -> Evaluated:
        """Evaluate in the given context."""

    def serialize(self) -> Expression:
        """Serialize to raw expression"""

    def simplify(self, context: Context) -> Evaluated | Evaluable:
        """Serialize to raw expression"""

    def __str__(self) -> str:
        """Get statement from of expression"""


def flatten_context(context: Context) -> Context:
    """
    Flatten context into a map of map[property path]value.

    Example:

    context = {
        "name":    "peter",
        "options": [1, 2, 3],
        "address": {
            "city":    "Toronto",
            "country": "Canada",
        },
    }

    flattened = flatten_context(ctx)

    {
        "name":    "peter",
        "options[0]": 1,
        "options[1]": 2,
        "options[2]": 3,
        "address.city": "Toronto",
        "address.country": "Canada",
    }
    """

    res = {}

    def join_path(left: str, right: str) -> str:
        return right if len(left) == 0 else f"{left}.{right}"

    def lookup(subject, path: str):
        if isinstance(subject, (int, float, str, bool)):
            res[path] = subject
        if isinstance(subject, dict):
            for key, val in subject.items():
                lookup(val, join_path(path, key))
        if isinstance(subject, (list, set, tuple)):
            for index, item in enumerate(subject):
                lookup(item, f"{path}[{index}]")

    lookup(context, "")
    return res
