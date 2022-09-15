from datetime import date
from typing import Protocol
from dateutil.relativedelta import relativedelta
from example.indicator_services import MindicadorService


class ReadjustProtocol(Protocol):
    def readjust_percentage(self, months) -> float:
        ...


class IPCReadjust(ReadjustProtocol):
    def __init__(self) -> None:
        self._indicator_service = MindicadorService()

    def readjust_percentage(self, months) -> float:
        ipc_values = self.__get_ipc(months)

        return sum(ipc_values) / 100

    def __get_ipc(self, months):
        date_to = date.today()
        date_from = date_to - relativedelta(months=months)

        return self._indicator_service.get_ipc_values(date_from, date_to)


class UFReadjust(ReadjustProtocol):
    def __init__(self) -> None:
        self._indicator_service = MindicadorService()

    def readjust_percentage(self, months) -> float:
        uf_values = self.__get_uf(months)

        return uf_values[0] / uf_values[1] - 1

    def __get_uf(self, months):
        date_to = date.today()
        date_from = date_to - relativedelta(months=months)

        return self._indicator_service.get_uf_values(date_from, date_to)
