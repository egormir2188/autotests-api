from bot.notification import send_telegram_message


def pytest_sessionfinish(session):
    passed = session.testscollected - session.testsfailed
    failed = session.testsfailed

    message = (
        f"{'🟢' if failed == 0 else '🔴'} API regression tests results:\n"
        f"Passed: {passed}\n"
        f"Failed: {failed}\n"
    )

    send_telegram_message(message)