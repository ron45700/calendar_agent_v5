import json
from collections import Counter
from datetime import datetime

from evals.load_cases import load_cases
from src.config.settings import TIMEZONE
from src.interpretation.parser import build_event_prompt, response_to_parseresult
from src.models.parse_result import ParseResult
from src.models.status import Status
from src.services.fake_client import send_fake_msg
from src.services.openai_client import send_prompt
from src.services.send_msg_model import Model, send_message


def run_evals(
    model: Model,
) -> tuple[list[tuple[str, str, str, ParseResult | None]], Counter]:
    results_list = []

    for case in load_cases("evals/cases.json"):
        result_type = ""
        test_type = ""
        reason = "None"
        obj = None
        expected_status = Status(case["expected_status"])

        if case["test_type"].strip() == "chain":
            txt, schema = build_event_prompt(
                raw_text=case["raw_text"],
                now=datetime.fromisoformat(case["now"]),
                timezone=TIMEZONE,
            )
            response = send_message(model=model, prompt=txt, schema=schema)
            result = response_to_parseresult(response=response)
            result_status = result.status
            test_type = case["test_type"].strip()
            obj = result

            if (
                result_status == expected_status
                and expected_status == Status.NEED_CLARIFICATION
            ):
                if result.need_clarification is None:
                    result_type = "failed"
                    reason = "there is not need_clarification message"
                else:
                    result_type = "pass"

            elif result_status == expected_status and expected_status == Status.OK:
                if result.event.start == datetime.fromisoformat(
                    case["expected_event"]["start"]
                ) and result.event.end == datetime.fromisoformat(
                    case["expected_event"]["end"]
                ):
                    result_type = "pass"
                else:
                    result_type = "failed"
                    reason = f"dates are not matched. start date -  got: {result.event.start} , expected: {case['expected_event']['start']}.  end date -  got: {result.event.end} , expected: {case['expected_event']['end']}"

            else:
                result_type = "failed"
                reason = f"status does not match. got: {result_status} , expected: {case['expected_status']}"

        elif case["test_type"].strip() == "parser":
            result = response_to_parseresult(json.dumps(case["fake_response"]))
            result_status = result.status
            test_type = case["test_type"].strip()
            obj = result
            if result_status == expected_status:
                if result_status == Status.OK:
                    result_type = "pass"
                elif result_status == Status.FAILED:
                    if result.exception is None:
                        result_type = "failed"
                        reason = "there is no exception explaination from response"
                    elif result.exception.startswith(case["reason"]):
                        result_type = "pass"
                    else:
                        result_type = "failed"
                        reason = f"reason does not match. got: {result.exception} , expected: {case['reason']}"

                elif result_status == Status.NEED_CLARIFICATION:
                    if result.need_clarification is None:
                        result_type = "failed"
                        reason = "there is not clarification message"
                    else:
                        result_type = "pass"
            else:
                result_type = "failed"
                reason = f"status does not match. got: {result_status} , expected: {case['expected_status']}"

        else:
            result_type = "failed"
            test_type = case["test_type"].strip()
            reason = "test_type NOT RECONIZED"
            obj = None

        results_list.append((result_type, test_type, reason, obj))

    results_list.sort(key=lambda s: (s[0], s[1]))
    count_results = Counter((s[0], s[1]) for s in results_list)

    return results_list, count_results


if __name__ == "__main__":

    def print_results(model: Model, txt: str) -> None:
        print(f"\n {txt} \n\n")
        results, count = run_evals(model)
        for item in sorted(count.items(), key=lambda item: item[0]):
            print(f"{item}")

        print()
        for result in results:
            print(f"{result}\n")

    print_results(send_prompt, "run evals test on real model:")
    print_results(send_fake_msg, "run evals test on fake model:")
