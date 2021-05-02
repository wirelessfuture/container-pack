class RotationTypeAny:
    RT_WHD = 0
    RT_HWD = 1
    RT_HDW = 2
    RT_DHW = 3
    RT_DWH = 4
    RT_WDH = 5

    ALL = [RT_WHD, RT_HWD, RT_HDW, RT_DHW, RT_DWH, RT_WDH]


class RotationTypeRightWayUp:
    RT_WHD = 0
    RT_DHW = 1

    ALL = [RT_WHD, RT_DHW]


class Axis:
    WIDTH = 0
    HEIGHT = 1
    DEPTH = 2

    ALL = [WIDTH, HEIGHT, DEPTH]


DEFAULT_PRECISION = 2
