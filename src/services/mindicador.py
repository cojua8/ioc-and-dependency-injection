from datetime import date
import requests

from models.mindicador_models import MindicadorModels
from services.indicator_service_protocol import IndicatorServiceProtocol


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

        return MindicadorModels.from_json(response.json())
