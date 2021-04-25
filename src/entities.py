from dataclasses import dataclass


@dataclass
class DimensionsD:
    width: [float, int]
    height: [float, int]
    depth: [float, int]
