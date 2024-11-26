import json
import matplotlib.pyplot as plt
import numpy as np
import os
from random import randint

MIN_INDEX = 0
MAX_INDEX = -1
STEP = 0

def moving_average(a, n=10):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

if __name__ == '__main__':
    all_files = os.listdir("data")
    all_files.sort()
    all_files = list(filter(lambda x: x.split(".")[1] == "bmespecimen", all_files))

    colors = []

    for i in range(len(all_files)):
        colors.append('#%06X' % randint(0, 0xFFFFFF))

    data = []

    for file_name in all_files:
        with open(f"data/{file_name}", "r") as file:
            # TODO: TAKE AVERAGE OF ALL 8 SENSORS
            json_data = json.load(file)
            specimen_data = list(filter(lambda x: x[8] == STEP, json_data["data"]["specimenDataPoints"][MIN_INDEX:MAX_INDEX]))

            gas_array = np.array(list(map(lambda x: x[1], specimen_data)))
            gas_moving_average = moving_average(gas_array)

            timestamp_array = np.array(list(map(lambda x: x[5], specimen_data)))[:-9]   # This is necessary because of the moving average calculations

            temp_array = np.array(list(map(lambda x: x[2], specimen_data)))
            temp_moving_average = moving_average(temp_array)

            data.append({
                "name": f"{file_name.split('_')[0]}% Ethanol",
                "color": colors.pop(),
                "gas": gas_moving_average,
                "temp": temp_moving_average,
                "timestamp": timestamp_array
            })

    fig, ax1 = plt.subplots()

    ax1.set_ylabel('Gas Resistance')
    # ax2 = ax1.twinx()
    # ax2.set_ylabel('Temperature')

    for d in data:
        ax1.plot(d["timestamp"], d["gas"], color=d["color"], label=d["name"], linestyle="None", marker=".", markersize=2)
        # ax2.plot(d["temp"], color=d["color"], label=d["name"], linestyle="dotted")

    ax1.legend(markerscale=10)
    plt.show()
