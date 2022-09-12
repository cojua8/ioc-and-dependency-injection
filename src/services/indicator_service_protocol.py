from typing import List, Protocol


class IndicatorServiceProtocol(Protocol):
    def get_ipc_values(self, date_from, date_to) -> List[float]:
        ...

    def get_uf_values(self, date_from, date_to) -> List[float]:
        ...
