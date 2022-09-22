from dependency_injector.wiring import Provide, inject


class Readjuster:
    @inject
    def __init__(
        self,
        amount,
        months,
        readjust_calculator=Provide["readjuster_service"],
    ) -> None:
        self._amount = amount
        self._months = months
        self._readjust_calculator = readjust_calculator

    def calculate(self) -> float:
        readjust_percentage = self._readjust_calculator.readjust_percentage(
            self._months
        )

        return round(self._amount * (readjust_percentage + 1), 2)
