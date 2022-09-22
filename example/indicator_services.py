from datetime import date
from typing import List, Protocol
from dependency_injector.wiring import Provide, inject
import requests

# from example.container import Container #esto haria un import circular

from example.indicator_models import CentralBankResponse, MindicadorResponse


class IndicatorServiceProtocol(Protocol):
    def get_ipc_values(self, date_from, date_to) -> List[float]:
        ...

    def get_uf_values(self, date_from, date_to) -> List[float]:
        ...


class MindicadorService(IndicatorServiceProtocol):
    def __init__(self) -> None:
        self._base_url = "https://mindicador.cl/api"

    def get_ipc_values(self, date_from, date_to):
        ipc_values = self.__get_values("ipc")

        return [
            v.valor for v in ipc_values.serie if date_from <= v.fecha.date() <= date_to
        ]

    def get_uf_values(self, date_from, date_to):
        uf_values = self.__get_values("uf")
        return [
            v.valor for v in uf_values.serie if v.fecha.date() in [date_to, date_from]
        ]

    def __get_values(self, indicator):
        year = date.today().year

        response = requests.get(f"{self._base_url}/{indicator}/{year}")

        response.raise_for_status()

        return MindicadorResponse.from_json(response.json())


class BancoCentralService(IndicatorServiceProtocol):
    @inject
    def __init__(
        self,
        user: str = Provide["config.bcentral_user"],
        password: str = Provide["config.bcentral_pass"],
    ) -> None:
        self._base_url = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx"
        self._user = user
        self._password = password

    def get_ipc_values(self, date_from, date_to):
        ipc_values = self.__get_values("F074.IPC.VAR.Z.Z.C.M")

        return [
            v.value
            for v in ipc_values.series.obs
            if date_from <= v.index_date_string.date() <= date_to
        ]

    def get_uf_values(self, date_from, date_to):
        uf_values = self.__get_values("F073.UFF.PRE.Z.D")

        return [
            v.value
            for v in uf_values.series.obs
            if v.index_date_string.date() in [date_to, date_from]
        ]

    def __get_values(self, series):
        date_from = date(date.today().year, 1, 1).strftime("%Y-%m-%d")

        response = requests.get(
            self._base_url,
            params={
                "user": self._user,
                "pass": self._password,
                "firstdate": date_from,
                "timeseries": series,
            },
        )

        response.raise_for_status()

        return CentralBankResponse.from_json(response.json())
