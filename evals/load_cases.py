import json
from collections.abc import Iterator


def load_cases(path: str) -> Iterator[dict]:
    with open(path, "r", encoding="utf-8") as f:
        cases = json.load(f)

    yield from cases


if __name__ == "__main__":
    for case in load_cases("evals/cases.json"):
        print(
            f'type:{case["test_type"]}, name:{case["name"]} -> {case["expected_status"]}'
        )
