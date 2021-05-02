from typing import List, Dict
from base_types import ShippableT
from entities import DimensionsD
from constants import RotationTypeAny, RotationTypeRightWayUp, DEFAULT_PRECISION
from helpers import set_to_decimal
from enums import CARGO_TYPE


class ShippableC(ShippableT):
    """The basic shippable class."""

    def __init__(
        self,
        name: str,
        stackable: bool,
        cargo_type: CARGO_TYPE,
        dimensions: DimensionsD,
        weight: [float, int],
        right_way_up: bool,
    ) -> None:
        self.name = name
        self.stackable = stackable
        self.cargo_type = cargo_type

        self.dimensions = dimensions
        self.dimensions.width = set_to_decimal(dimensions.width, DEFAULT_PRECISION)
        self.dimensions.height = set_to_decimal(dimensions.height, DEFAULT_PRECISION)
        self.dimensions.depth = set_to_decimal(dimensions.depth, DEFAULT_PRECISION)
        self.weight = set_to_decimal(weight, DEFAULT_PRECISION)
        self.right_way_up = right_way_up

        self.rotation_type = 0
        self.position = [0, 0, 0]

    def describe(self) -> Dict:
        """Returns a dict with shippable characteristics."""
        return dict(
            name=self.name,
            width=float(self.dimensions.width),
            height=float(self.dimensions.height),
            depth=float(self.dimensions.depth),
            weight=float(self.weight),
            right_way_up=self.right_way_up,
            position=[float(x) for x in self.position],
            rotation_type=self.rotation_type,
            volume=float(self.get_volume()),
            stackable=self.stackable,
        )

    def get_volume(self) -> [float, int]:
        """Returns the volume^^3 of the shippable."""
        return set_to_decimal(
            self.dimensions.width * self.dimensions.height * self.dimensions.depth,
            DEFAULT_PRECISION,
        )

    def get_dimension(self) -> list:
        """Returns the next dimension."""
        if self.right_way_up:
            if self.rotation_type == RotationTypeRightWayUp.RT_WHD:
                dimension = [
                    self.dimensions.width,
                    self.dimensions.height,
                    self.dimensions.depth,
                ]
            elif self.rotation_type == RotationTypeRightWayUp.RT_DHW:
                dimension = [
                    self.dimensions.depth,
                    self.dimensions.height,
                    self.dimensions.width,
                ]
            else:
                dimension = []

        elif not self.right_way_up:
            if self.rotation_type == RotationTypeAny.RT_WHD:
                dimension = [
                    self.dimensions.width,
                    self.dimensions.height,
                    self.dimensions.depth,
                ]
            elif self.rotation_type == RotationTypeAny.RT_HWD:
                dimension = [
                    self.dimensions.height,
                    self.dimensions.width,
                    self.dimensions.depth,
                ]
            elif self.rotation_type == RotationTypeAny.RT_HDW:
                dimension = [
                    self.dimensions.height,
                    self.dimensions.depth,
                    self.dimensions.width,
                ]
            elif self.rotation_type == RotationTypeAny.RT_DHW:
                dimension = [
                    self.dimensions.depth,
                    self.dimensions.height,
                    self.dimensions.width,
                ]
            elif self.rotation_type == RotationTypeAny.RT_DWH:
                dimension = [
                    self.dimensions.depth,
                    self.dimensions.width,
                    self.dimensions.height,
                ]
            elif self.rotation_type == RotationTypeAny.RT_WDH:
                dimension = [
                    self.dimensions.width,
                    self.dimensions.depth,
                    self.dimensions.height,
                ]
            else:
                dimension = []

        return dimension
