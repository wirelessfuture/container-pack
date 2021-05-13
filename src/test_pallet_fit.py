import json
import pytest
from loader import Loader
from shippable import ShippableC
from container import ContainerC
from entities import DimensionsD
from enums import CARGO_TYPE

"""
TESTS
* Test that various pallet groups will fit to their prospective container as follows:
* 20" Standard should be able to fit 10 Standard or 11 Euro Pallets
* 40" Standard should be able to fit 21 Standard or 25 Euro Pallets
* 40" Palletwide should be able to fit 24 Standard or 30 Euro Pallets
* 45" Standard should be ablt to fit 24 Standard or 27 Euro Pallets
* 45" Palletwide should be able to fit 26 Standard or 33 Euro Pallets
NOTE: That this is for 1 layer
TODO: Create a base test class
"""


class TestStandard20:
    def test_standard_stackable(self):
        loader = Loader()
        loader.add_container(
            ContainerC(
                "Standard 20",
                CARGO_TYPE.STANDARD,
                DimensionsD(width=235.2, height=239.5, depth=590),
                28130,
            )
        )

        for i in range(10):
            loader.add_shippable(
                ShippableC(
                    f"Standard-Pallet-Stackable-{i}",
                    False,
                    CARGO_TYPE.STANDARD,
                    DimensionsD(width=120, height=100, depth=100),
                    80,
                    True,
                )
            )

        loader.load()

        container = loader.containers[0]
        unfitted_len = len(container.unfitted_shippables)
        assert unfitted_len == 0

    def test_euro_stackable(self):
        loader = Loader()
        loader.add_container(
            ContainerC(
                "Standard 20",
                CARGO_TYPE.STANDARD,
                DimensionsD(width=235.2, height=239.5, depth=590),
                28130,
            )
        )

        for i in range(22):
            loader.add_shippable(
                ShippableC(
                    f"Euro-Pallet-Stackable-{i}",
                    True,
                    CARGO_TYPE.STANDARD,
                    DimensionsD(width=120, height=100, depth=80),
                    80,
                    True,
                )
            )

        loader.load()

        container = loader.containers[0]
        unfitted_len = len(container.unfitted_shippables)
        assert unfitted_len == 0
