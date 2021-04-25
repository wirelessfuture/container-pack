from typing import List
from base_types import ShippableT
from constants import RotationType, Axis, DEFAULT_PRECISION
from helpers import intersect, set_to_decimal


class Loader:
    def __init__(self) -> None:
        self.containers = []
        self.shippables = []
        self.unfit_shippables = []
        self.total_shippables = 0

    def add_container(self, container) -> None:
        """Registers a new container in the loader."""
        return self.containers.append(container)

    def add_shippable(self, shippable) -> None:
        """Registers a new shippable in the loader."""
        self.total_shippables = len(self.shippables) + 1

        return self.shippables.append(shippable)

    def load_to_container(self, container, shippable) -> None:
        """Attempts to load all shippables to the container."""
        fitted = False

        if not container.shippables:
            response = container.put_shippable(shippable, [0, 0, 0])

            if not response:
                container.unfitted_shippables.append(shippable)

            return

        for axis in range(0, 3):
            shippables_in_container = container.shippables

            for ib in shippables_in_container:
                pivot = self.get_pivot(axis, ib, shippable)

                if container.put_shippable(shippable, pivot):
                    fitted = True
                    break
            if fitted:
                break

        if not fitted:
            container.unfitted_shippables.append(shippable)

    def get_pivot(self, axis: Axis, ib: ShippableT, shippable: ShippableT) -> List[int]:
        """Returns the next pivot."""
        pivot = [0, 0, 0]
        w, h, d = ib.get_dimension()
        if axis == Axis.WIDTH:
            pivot = [ib.position[0] + w, ib.position[1], ib.position[2]]
        elif axis == Axis.HEIGHT and shippable.stackable:
            pivot = [ib.position[0], ib.position[1] + h, ib.position[2]]
        elif axis == Axis.HEIGHT and not shippable.stackable:
            pivot = [ib.position[0], ib.position[1], ib.position[2]]
        elif axis == Axis.DEPTH:
            pivot = [ib.position[0], ib.position[1], ib.position[2] + d]

        return pivot

    def load(
        self,
        bigger_first=False,
        distribute_shippables=False,
        number_of_decimals=DEFAULT_PRECISION,
    ) -> None:
        """Attempts to load all shippables to all containers registered."""

        self.containers.sort(
            key=lambda container: container.get_volume(), reverse=bigger_first
        )
        self.shippables.sort(
            key=lambda shippable: shippable.get_volume(), reverse=bigger_first
        )

        for container in self.containers:
            for shippable in self.shippables:
                self.load_to_container(container, shippable)

            if distribute_shippables:
                for shippable in container.shippables:
                    self.shippables.remove(shippable)
