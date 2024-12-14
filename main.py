from matplotlib import colormaps
from scipy import stats

import json
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

def parse_ethanol_label(file_n: str):
    concentration = file_n.split('_')[0]
    added_information = file_n.split('-')
    if len(added_information) == 1:
        hint = ''
    else:
        hint = f"({added_information[-1].split('.')[0]})"

    return f"{concentration}% Ethanol {hint}"

def parse_diacetyl_label(file_n: str):
    concentration = file_n.split('_')[0]
    added_information = file_n.split('-')
    if len(added_information) == 1:
        hint = ''
    else:
        hint = f"({added_information[-1].split('.')[0]})"

    return f"{concentration}ppm Diacetyl {hint}"

if __name__ == '__main__':
    all_files = get_specimen_files("data")
    colors = get_random_colors(len(all_files))

    ethanol_data = []
    diacetyl_data = []

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

            gas = np.array(gas)
            temp = np.array(temp)
            pressure = np.array(pressure)
            humidity = np.array(humidity)

            gas_moving_average = moving_average(gas)
            temp_moving_average = moving_average(temp)
            pressure_moving_average = moving_average(pressure)
            humidity_moving_average = moving_average(humidity)

            temp_z = stats.zscore(temp_moving_average)
            pressure_z = stats.zscore(pressure_moving_average)
            humidity_z = stats.zscore(humidity_moving_average)

            # gas_adjusted_with_z_score = np.multiply(gas_moving_average, temp_z)
            # gas_adjusted_with_z_score = np.multiply(gas_adjusted_with_z_score, temp_z)
            # gas_adjusted_with_z_score = np.multiply(gas_adjusted_with_z_score, pressure_z)
            # gas_adjusted_with_z_score = np.multiply(gas_adjusted_with_z_score, humidity_z)

            if "ethanol" in file_name:
                ethanol_data.append({
                    "name": parse_ethanol_label(file_name),
                    "color": colors.pop(),
                    "gas": gas_moving_average,
                    "temp": temp_moving_average,
                    "pressure": pressure_moving_average,
                    "humidity": humidity_moving_average,
                    "timestamp": time_since_power_on[:-(AVG_N - 1)] # This is necessary because of the moving average calculations
                })

            elif "diacetyl" in file_name:
                diacetyl_data.append({
                    "name": parse_diacetyl_label(file_name),
                    "color": colors.pop(),
                    "gas": gas_moving_average,
                    "temp": temp_moving_average,
                    "pressure": pressure_moving_average,
                    "humidity": humidity_moving_average,
                    "timestamp": time_since_power_on[:-(AVG_N - 1)]
                    # This is necessary because of the moving average calculations
                })

            else:
                continue

    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Time since power on (ms)')
    ax1.set_ylabel('Gas Resistance (Moving Average) - Ethanol')

    # ax2.set_xlabel('Time since power on (ms)')
    # ax2.set_ylabel('Gas Resistance (Moving Average) - Diacetyl')

    for d in ethanol_data:
        ax1.plot(d["timestamp"], d["gas"], color=d["color"], label=d["name"], linestyle="None", marker=".",
                 markersize=2)

    '''
    for d in diacetyl_data:
        ax2.plot(d["timestamp"], d["gas"], color=d["color"], label=d["name"], linestyle="None", marker=".",
                 markersize=2)
     '''

    ax1.legend(markerscale=10, loc=1)
    # ax2.legend(markerscale=10, loc=1)

    plt.show()
