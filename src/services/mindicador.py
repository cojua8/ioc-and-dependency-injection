from datetime import date
import requests

from models.mindicador_models import MindicadorModels


class MindicadorService:
    def __init__(self) -> None:
        self._base_url = "https://mindicador.cl/api"

    def get_ipc_values(self):
        return self.__get_values("ipc")

    def get_uf_values(self):
        return self.__get_values("uf")

    def __get_values(self, indicator):
        year = date.today().year

        response = requests.get(f"{self._base_url}/{indicator}/{year}")

        response.raise_for_status()

        return MindicadorModels.from_json(response.json())
