from datetime import date
from typing import Protocol
from dateutil.relativedelta import relativedelta

from services.indicator_service_protocol import IndicatorServiceProtocol


class ReadjustProtocol(Protocol):
    def readjust_percentage(self, months) -> float:
        ...


class Readjuster:
    def __init__(self, amount, months, readjust_calculator: ReadjustProtocol) -> None:
        self._amount = amount
        self._months = months
        self._readjust_calculator = readjust_calculator

    def calculate(self) -> float:
        readjust_percentage = self._readjust_calculator.readjust_percentage(
            self._months
        )

        return round(self._amount * (readjust_percentage + 1), 2)


class IPCReadjust(ReadjustProtocol):
    def __init__(self, indicator_service: IndicatorServiceProtocol) -> None:
        self._indicator_service = indicator_service

    def readjust_percentage(self, months) -> float:
        ipc_values = self.__get_ipc(months)

        return sum(ipc_values) / 100

    def __get_ipc(self, months):
        date_to = date.today()
        date_from = date_to - relativedelta(months=months)

        return self._indicator_service.get_ipc_values(date_from, date_to)


class UFReadjust(ReadjustProtocol):
    def __init__(self, indicator_service: IndicatorServiceProtocol) -> None:
        self._indicator_service = indicator_service

    def readjust_percentage(self, months) -> float:
        uf_values = self.__get_uf(months)

        return uf_values[0] / uf_values[1] - 1

    def __get_uf(self, months):
        date_to = date.today()
        date_from = date_to - relativedelta(months=months)

        return self._indicator_service.get_uf_values(date_from, date_to)
