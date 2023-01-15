class ProgressTracker:
    def __init__(self):
        self.total = 0
        self.passed = 0
        self.failed = 0
        self.error_messages = list()

    def inc_success(self) -> None:
        self.total += 1
        self.passed += 1
        self.report()

    def inc_fail(self) -> None:
        self.total += 1
        self.failed += 1

    def add_error_message(self, msg: str) -> None:
        self.error_messages.append(msg)
        self.inc_fail()
        self.report()

    def get_error_messages(self) -> list:
        return self.error_messages

    def report(self) -> None:
        if self.total > 0 and self.total % 1000 == 0:
            print("Tests run so far: " + str(self.total))

    def get_results(self) -> str:
        result = "\n  Tests passed: " + str(self.passed)
        result += "\n  Tests failed: " + str(self.failed)
        result += "\n  Total tests:  " + str(self.total)
        if self.total > 0:
            result += "\nPercentage correct: " + str(int(float(self.passed) / float(self.total) * 100)) + "%"

        return result

    def no_failures(self) -> bool:
        return self.failed == 0
