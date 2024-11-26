import json
import matplotlib.pyplot as plt
import numpy as np
import os
from random import randint

MIN_INDEX = 0
MAX_INDEX = 20000
STEP = 0

def get_gas_resistance(file_path: str):
    with open(file_path, "r") as f:
        json_data = json.load(f)
        specimen_data = list(filter(lambda x: x[8] == STEP, json_data["data"]["specimenDataPoints"][MIN_INDEX:MAX_INDEX]))
        return np.array(list(map(lambda x: x[1], specimen_data)))

if __name__ == '__main__':
    all_files = os.listdir("data")
    all_files = list(filter(lambda x: x.split(".")[1] == "bmespecimen", all_files))

    colors = []

    for i in range(len(all_files)):
        colors.append('#%06X' % randint(0, 0xFFFFFF))

    data = []

    for file in all_files:
        data.append({
            "name": f"{file.split('_')[0]}% Ethanol",
            "color": colors.pop(),
            "data": get_gas_resistance(f"data/{file}")
        })

    fig, ax = plt.subplots()

    ax.set_ylabel('Gas Resistance')
    for d in data:
        ax.plot(d["data"], color=d["color"], label=d["name"])

    ax.legend()

    fig.tight_layout()
    plt.show()
