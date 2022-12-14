from datetime import datetime
from typing import Any, List


class MindicadorSerie:
    fecha: datetime
    valor: float

    def __init__(self, fecha: datetime | str, valor: float) -> None:
        self.fecha = (
            datetime.strptime(fecha, "%Y-%m-%dT%H:%M:%S.%fZ")
            if isinstance(fecha, str)
            else fecha
        )
        self.valor = valor


class MindicadorResponse:
    version: str
    autor: str
    codigo: str
    nombre: str
    unidad_medida: str
    serie: List[MindicadorSerie]

    def __init__(
        self,
        version: str,
        autor: str,
        codigo: str,
        nombre: str,
        unidad_medida: str,
        serie: List[MindicadorSerie],
    ) -> None:
        self.version = version
        self.autor = autor
        self.codigo = codigo
        self.nombre = nombre
        self.unidad_medida = unidad_medida
        self.serie = serie

    @classmethod
    def from_json(cls, data):
        serie = [MindicadorSerie(**s) for s in data["serie"]]

        return cls(
            **{k: v for k, v in data.items() if k != "serie"},
            serie=serie,
        )


class CentralBank:
    index_date_string: datetime
    value: float
    status_code: str

    def __init__(
        self, index_date_string: str | datetime, value: str, status_code: str
    ) -> None:
        if isinstance(index_date_string, str):
            self.index_date_string = datetime.strptime(index_date_string, "%d-%m-%Y")
        self.value = value
        self.status_code = status_code

    @classmethod
    def from_json(cls, json_data):
        return cls(
            json_data["indexDateString"],
            float(json_data["value"]),
            json_data["statusCode"],
        )


class CentralBankSeries:
    descrip_esp: str
    descrip_ing: str
    series_id: str
    obs: List[CentralBank]

    def __init__(
        self, descrip_esp: str, descrip_ing: str, series_id: str, obs: List[CentralBank]
    ) -> None:
        self.descrip_esp = descrip_esp
        self.descrip_ing = descrip_ing
        self.series_id = series_id
        self.obs = obs

    @classmethod
    def from_json(cls, json_data):
        obs = [CentralBank.from_json(v) for v in json_data["Obs"]]
        obs.reverse()

        return cls(
            json_data["descripEsp"], json_data["descripIng"], json_data["seriesId"], obs
        )


class CentralBankResponse:
    codigo: int
    descripcion: str
    series: CentralBankSeries
    series_infos: List[Any]

    def __init__(
        self,
        codigo: int,
        descripcion: str,
        series: CentralBankSeries,
        series_infos: List[Any],
    ) -> None:
        self.codigo = codigo
        self.descripcion = descripcion
        self.series = series
        self.series_infos = series_infos

    @classmethod
    def from_json(cls, json_data):
        return cls(
            json_data["Codigo"],
            json_data["Descripcion"],
            CentralBankSeries.from_json(json_data["Series"]),
            json_data["SeriesInfos"],
        )
