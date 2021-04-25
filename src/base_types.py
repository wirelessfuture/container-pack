from typing import Dict
from abc import ABC, abstractmethod


class ShippableT(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def describe(self) -> Dict:
        pass

    @abstractmethod
    def get_volume(self) -> float:
        pass

    @abstractmethod
    def get_dimension(self) -> list:
        pass


class ContainerT(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def describe(self) -> Dict:
        pass

    @abstractmethod
    def get_volume(self) -> float:
        pass

    @abstractmethod
    def get_total_weight(self) -> float:
        pass

    @abstractmethod
    def put_shippable(self) -> bool:
        pass
