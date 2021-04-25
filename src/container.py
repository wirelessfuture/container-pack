from typing import List, Dict
from base_types import ContainerT
from constants import RotationType, DEFAULT_PRECISION
from helpers import intersect, set_to_decimal
from entities import DimensionsD
from enums import CARGO_TYPE


class ContainerC(ContainerT):
    def __init__(
        self,
        name: str,
        cargo_type: CARGO_TYPE,
        inside_dimensions: DimensionsD,
        max_payload: int,
    ) -> None:
        self.name = name
        self.cargo_type = cargo_type

        self.inside_dimensions = inside_dimensions
        self.inside_dimensions.width = set_to_decimal(
            inside_dimensions.width, DEFAULT_PRECISION
        )
        self.inside_dimensions.height = set_to_decimal(
            inside_dimensions.height, DEFAULT_PRECISION
        )
        self.inside_dimensions.depth = set_to_decimal(
            inside_dimensions.depth, DEFAULT_PRECISION
        )

        self.max_payload = set_to_decimal(max_payload, DEFAULT_PRECISION)

        self.shippables = []
        self.unfitted_shippables = []

    def describe(self) -> Dict:
        """Returns a dict with container characteristics."""
        return dict(
            name=self.name,
            width=float(self.inside_dimensions.width),
            height=float(self.inside_dimensions.height),
            depth=float(self.inside_dimensions.depth),
            weight=float(self.max_payload),
            volume=float(self.get_volume()),
        )

    def get_volume(self) -> float:
        """Returns the container volume^^3."""
        return set_to_decimal(
            self.inside_dimensions.width
            * self.inside_dimensions.height
            * self.inside_dimensions.depth,
            DEFAULT_PRECISION,
        )

    def get_total_weight(self) -> float:
        """Returns the total shippable payload volume^^3."""
        total_weight = 0
        for shippable in self.shippables:
            total_weight += shippable.weight

        return set_to_decimal(total_weight, DEFAULT_PRECISION)

    def put_shippable(self, shippable, pivot) -> bool:
        """Calculates if the shippable will fit."""
        fit = False
        valid_shippable_position = shippable.position
        shippable.position = pivot

        for i in range(0, len(RotationType.ALL)):
            shippable.rotation_type = i
            dimension = shippable.get_dimension()
            if (
                self.inside_dimensions.width < pivot[0] + dimension[0]
                or self.inside_dimensions.height < pivot[1] + dimension[1]
                or self.inside_dimensions.depth < pivot[2] + dimension[2]
            ):
                continue

            fit = True

            for current_shippable_in_container in self.shippables:
                if intersect(current_shippable_in_container, shippable):
                    fit = False
                    break

            if fit:
                if self.get_total_weight() + shippable.weight > self.max_payload:
                    fit = False
                    return fit

                self.shippables.append(shippable)

            if not fit:
                shippable.position = valid_shippable_position

            return fit

        if not fit:
            shippable.position = valid_shippable_position

        return fit
