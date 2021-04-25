from constants import RotationType, Axis, DEFAULT_PRECISION
from helpers import intersect, set_to_decimal


class Packer:
    def __init__(self):
        self.containers = []
        self.shippables = []
        self.unfit_shippables = []
        self.total_shippables = 0

    def add_container(self, container):
        return self.containers.append(container)

    def add_shippable(self, shippable):
        self.total_shippables = len(self.shippables) + 1

        return self.shippables.append(shippable)

    def pack_to_container(self, container, shippable):
        fitted = False

        if not container.shippables:
            response = container.put_shippable(shippable, [0, 0, 0])

            if not response:
                container.unfitted_shippables.append(shippable)

            return

        for axis in range(0, 3):
            shippables_in_container = container.shippables

            for ib in shippables_in_container:
                pivot = [0, 0, 0]
                w, h, d = ib.get_dimension()
                if axis == Axis.WIDTH:
                    pivot = [ib.position[0] + w, ib.position[1], ib.position[2]]
                elif axis == Axis.HEIGHT and shippable.stackable: # If the container is stackable we can pivot the HEIGHT axis
                    pivot = [ib.position[0], ib.position[1] + h, ib.position[2]]
                elif axis == Axis.DEPTH:
                    pivot = [ib.position[0], ib.position[1], ib.position[2] + d]

                if container.put_shippable(shippable, pivot):
                    fitted = True
                    break
            if fitted:
                break

        if not fitted:
            container.unfitted_shippables.append(shippable)

    def pack(
        self,
        bigger_first=False,
        distribute_shippables=False,
        number_of_decimals=DEFAULT_PRECISION,
    ):

        self.containers.sort(
            key=lambda container: container.get_volume(), reverse=bigger_first
        )
        self.shippables.sort(
            key=lambda shippable: shippable.get_volume(), reverse=bigger_first
        )

        for container in self.containers:
            for shippable in self.shippables:
                self.pack_to_container(container, shippable)

            if distribute_shippables:
                for shippable in container.shippables:
                    self.shippables.remove(shippable)
