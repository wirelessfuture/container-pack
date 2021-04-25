import json
from packer import Packer
from shippable import ShippableC
from container import ContainerC
from entities import DimensionsD


packer = Packer()

packer.add_container(
    ContainerC("Standard 20", DimensionsD(width=235.2, height=239.5, depth=590), 28130)
)
packer.add_container(
    ContainerC(
        "Standard 40", DimensionsD(width=235.2, height=239.5, depth=1203.2), 28750
    )
)
packer.add_container(
    ContainerC(
        "Standard 45 High Cube",
        DimensionsD(width=235.2, height=270, depth=1355.6),
        27700,
    )
)

for i in range(22):
    packer.add_shippable(
        ShippableC(
            f"Euro-Pallet-{i}",
            DimensionsD(width=80, height=100, depth=120),
            80,
            True,
        )
    )

packer.pack()

results = {"results": []}
for c in packer.containers:
    data = {}
    data["container"] = c.describe()
    data["fitted_shippables"] = [shippable.describe() for shippable in c.shippables]
    data["unfitted_shippables"] = [
        unfitted_shippable.describe()
        for unfitted_shippable in c.unfitted_shippables
        if len(c.unfitted_shippables) <= 0
    ]
    results["results"].append(data)


for r in results["results"]:
    for k, v in r["container"].items():
        if v == "Standard 20":
            print(json.dumps(r, indent=4))