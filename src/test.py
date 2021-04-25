import json
from loader import Loader
from shippable import ShippableC
from container import ContainerC
from entities import DimensionsD
from enums import CARGO_TYPE


loader = Loader()

loader.add_container(
    ContainerC(
        "Standard 20",
        CARGO_TYPE.STANDARD,
        DimensionsD(width=235.2, height=239.5, depth=590),
        28130,
    )
)
loader.add_container(
    ContainerC(
        "Standard 40",
        CARGO_TYPE.STANDARD,
        DimensionsD(width=235.2, height=239.5, depth=1203.2),
        28750,
    )
)
loader.add_container(
    ContainerC(
        "Standard 40 High Cube",
        CARGO_TYPE.STANDARD,
        DimensionsD(width=235, height=270, depth=1203.2),
        28600,
    )
)
loader.add_container(
    ContainerC(
        "Standard 45 High Cube",
        CARGO_TYPE.STANDARD,
        DimensionsD(width=235.2, height=270, depth=1355.6),
        27700,
    )
)

for i in range(11):
    loader.add_shippable(
        ShippableC(
            f"Euro-Pallet-Unstackable-{i}",
            False,
            CARGO_TYPE.STANDARD,
            DimensionsD(width=120, height=100, depth=80),
            80,
        )
    )

for i in range(11):
    loader.add_shippable(
        ShippableC(
            f"Euro-Pallet-Stackable-{i}",
            True,
            CARGO_TYPE.STANDARD,
            DimensionsD(width=120, height=100, depth=80),
            80,
        )
    )

loader.load()

results = {"results": []}
for c in loader.containers:
    data = {}
    data["container"] = c.describe()
    data["fitted_shippables"] = [shippable.describe() for shippable in c.shippables]
    data["unfitted_shippables"] = [
        unfitted_shippable.describe() for unfitted_shippable in c.unfitted_shippables
    ]
    results["results"].append(data)


for res in results["results"]:
    if len(res["unfitted_shippables"]) > 0:
        print("DOES NOT FIT")
        print(res["container"]["name"])
        print("\n")
    else:
        print("DOES FIT")
        print(res["container"]["name"])
        print("\n")
