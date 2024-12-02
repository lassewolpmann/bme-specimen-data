import json

from matplotlib import colormaps
import matplotlib.pyplot as plt
import numpy as np
import os

AVG_N = 800

def moving_average(a, n=AVG_N):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def get_specimen_files(dir_name: str) -> list:
    files = os.listdir(dir_name)
    files.sort()
    return list(filter(lambda x: x[-11:] == "bmespecimen", files))

def get_random_colors(n: int) -> list:
    return list(colormaps['jet'](np.linspace(0, 1, n)))

def parse_file_label(file_n: str):
    concentration = file_n.split('_')[0]
    added_information = file_n.split('-')
    if len(added_information) == 1:
        hint = ''
    else:
        hint = f"({added_information[-1].split('.')[0]})"

    return f"{concentration}% Ethanol {hint}"

if __name__ == '__main__':
    all_files = get_specimen_files("data")
    colors = get_random_colors(len(all_files))

    data = []

    for file_name in all_files:
        with open(f"data/{file_name}", "r") as file:
            json_data = json.load(file)

            specimen_data = json_data["data"]["specimenDataPoints"]
            specimen_sorted_by_time = sorted(specimen_data, key=lambda x: x[5])
            specimen_sorted_by_time = list(filter(lambda x: x[8] == 0, specimen_sorted_by_time))

            gas = []
            temp = []
            pressure = []
            humidity = []
            time_since_power_on = []

            for s in specimen_sorted_by_time:
                gas.append(s[1])
                temp.append(s[2])
                pressure.append(s[3])
                humidity.append(s[4])
                time_since_power_on.append(s[5])

            gas_moving_average = moving_average(gas)
            temp_moving_average = moving_average(temp)
            pressure_moving_average = moving_average(pressure)
            humidity_moving_average = moving_average(humidity)

            data.append({
                "name": parse_file_label(file_name),
                "color": colors.pop(),
                "gas": gas_moving_average,
                "temp": temp_moving_average,
                "pressure": pressure_moving_average,
                "humidity": humidity_moving_average,
                "timestamp": time_since_power_on[:-(AVG_N - 1)] # This is necessary because of the moving average calculations
            })

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    ax1.set_xlabel('Time since power on (ms)')
    ax1.set_ylabel('Gas Resistance (Moving Average)')

    ax2.set_xlabel('Time since power on (ms)')
    ax2.set_ylabel('Temperature')

    ax3.set_xlabel('Time since power on (ms)')
    ax3.set_ylabel('Relative Humidity')

    ax4.set_xlabel('Time since power on (ms)')
    ax4.set_ylabel('Pressure')

    for d in data:
        ax1.plot(d["timestamp"], d["gas"], color=d["color"], label=d["name"], linestyle="None", marker=".",
                 markersize=2)
        ax2.plot(d["timestamp"], d["temp"], color=d["color"], label=d["name"], linestyle="None", marker=".",
                 markersize=2)
        ax3.plot(d["timestamp"], d["humidity"], color=d["color"], label=d["name"], linestyle="None", marker=".",
                 markersize=2)
        ax4.plot(d["timestamp"], d["pressure"], color=d["color"], label=d["name"], linestyle="None", marker=".",
                 markersize=2)

    ax1.legend(markerscale=10, loc=1)
    ax2.legend(markerscale=10, loc=1)
    ax3.legend(markerscale=10, loc=1)
    ax4.legend(markerscale=10, loc=1)

    plt.show()
