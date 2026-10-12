import csv
from pathlib import Path

import pytest

from assistant.rules import reply


with (Path(__file__).resolve().parents[1] / "eval" / "cases.csv").open(
    encoding="utf-8", newline=""
) as file:
    reader = csv.DictReader(file)
    FIELDS = reader.fieldnames
    CASES = list(reader)


def test_benchmark_format():
    assert FIELDS == ["question", "expected", "category"]
    assert len(CASES) == 15
    assert {case["category"] for case in CASES} == {
        "normal", "edge", "out-of-scope"
    }
    assert sum(case["category"] == "edge" for case in CASES) >= 3
    assert len({case["question"] for case in CASES}) == len(CASES)
    assert all(set(case) == set(FIELDS) and all(
        value is not None for value in case.values()
    ) and case["expected"] for case in CASES)


@pytest.mark.parametrize("case", CASES, ids=[
    f"{index}-{case['category']}" for index, case in enumerate(CASES, 1)
])
def test_benchmark_answer(case):
    assert reply(case["question"]) == case["expected"]
