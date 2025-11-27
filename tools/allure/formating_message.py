import json
import os
from typing import List, Dict, Tuple

def parse_allure_report(allure_report_dir: str) -> Tuple[int, int, int, List[Dict]]:
    """
    Парсит Allure-отчёт и возвращает количество успешных, упавших и сломанных тестов,
    а также список упавших и сломанных тестов с описанием ошибок.

    :param allure_report_dir: Директория с Allure-отчётом (обычно `allure-report`).
    :return: Кортеж (passed, failed, broken, failed_tests), где failed_tests — список словарей с информацией об упавших и сломанных тестах.
    """
    data_dir = os.path.join(allure_report_dir, "data")
    test_cases = os.path.join(data_dir, "test-cases")

    passed = 0
    failed = 0
    broken = 0
    failed_tests = []

    for test_case_file in os.listdir(test_cases):
        if test_case_file.endswith(".json"):
            with open(os.path.join(test_cases, test_case_file), "r") as f:
                test_case = json.load(f)

                if test_case["status"] == "passed":
                    passed += 1
                elif test_case["status"] == "failed":
                    failed += 1
                    failed_tests.append({
                        "name": test_case["name"],
                        "status": test_case["status"],
                        "failure_message": test_case.get("failure", {}).get("message", "Failure message not provided"),
                        "trace": test_case.get("failure", {}).get("trace", "No trace")
                    })
                elif test_case["status"] == "broken":
                    broken += 1
                    failed_tests.append({
                        "name": test_case["name"],
                        "status": test_case["status"],
                        "failure_message": test_case.get("failure", {}).get("message", "No failure message"),
                        "trace": test_case.get("failure", {}).get("trace", "No trace")
                    })

    return passed, failed, broken, failed_tests

def format_telegram_message(passed: int, failed: int, broken: int, failed_tests: List[Dict]) -> str:
    """
    Формирует сообщение для Telegram на основе данных из Allure-отчёта.

    :param passed: Количество успешных тестов.
    :param failed: Количество упавших тестов.
    :param broken: Количество сломанных тестов.
    :param failed_tests: Список словарей с информацией об упавших и сломанных тестах.
    :return: Отформатированное сообщение для Telegram.
    """
    emoji = "🟢" if failed == 0 and broken == 0 else "🔴"
    message = (
        f"{emoji} *API regression tests results:*\n\n"
        f"📊 *Results:*\n"
        f"✅ Passed: {passed}\n"
        f"❌ Failed: {failed}\n"
        f"🔧 Broken: {broken}\n"
    )

    if failed_tests and len(failed_tests) > 0:
        message += f"\n🔍 *Failed and Broken Tests:*\n"
        for i, test in enumerate(failed_tests, start=1):
            message += (
                f"{i}. *{test['name']}*\n"
                f"   Status: `{test['status']}`\n"
                f"   Message: `{test['failure_message']}`\n"
            )

    return message