from example.readjust_calculators import IPCReadjust


class Readjuster:
    def __init__(self, amount, months) -> None:
        self._amount = amount
        self._months = months
        self._readjust_calculator = IPCReadjust()

    def calculate(self) -> float:
        readjust_percentage = self._readjust_calculator.readjust_percentage(
            self._months
        )

        return round(self._amount * (readjust_percentage + 1), 2)
