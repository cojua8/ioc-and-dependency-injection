from datetime import date, datetime
from typing import List


class Serie:
    fecha: datetime
    valor: float

    def __init__(self, fecha: datetime | str, valor: float) -> None:
        self.fecha = (
            datetime.strptime(fecha, "%Y-%m-%dT%H:%M:%S.%fZ")
            if isinstance(fecha, str)
            else fecha
        )
        self.valor = valor


class MindicadorModels:
    version: str
    autor: str
    codigo: str
    nombre: str
    unidad_medida: str
    serie: List[Serie]

    def __init__(
        self,
        version: str,
        autor: str,
        codigo: str,
        nombre: str,
        unidad_medida: str,
        serie: List[Serie],
    ) -> None:
        self.version = version
        self.autor = autor
        self.codigo = codigo
        self.nombre = nombre
        self.unidad_medida = unidad_medida
        self.serie = serie

    @classmethod
    def from_json(cls, data):
        serie = [Serie(**s) for s in data["serie"]]

        return cls(
            **{k: v for k, v in data.items() if k != "serie"},
            serie=serie,
        )
