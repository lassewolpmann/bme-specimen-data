import json
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    with open("data/fresh_air_no_sample.bmespecimen", "r") as fresh_air_file:
        f = json.load(fresh_air_file)

        measurement_data = f["data"]["specimenDataPoints"][0:50000]
        gas = np.array(list(map(lambda x: x[1], measurement_data)))
        temp = np.array(list(map(lambda x: x[2], measurement_data)))
        time = np.array(list(map(lambda x: x[5], measurement_data)))

        fig, ax1 = plt.subplots()

        color = 'tab:red'
        ax1.set_xlabel('timestamp')
        ax1.set_ylabel('temp', color=color)
        ax1.set_ylim(bottom=0, top=temp.max())
        ax1.plot(time, temp, color=color)

        color = 'tab:blue'
        ax2 = ax1.twinx()
        ax2.set_ylabel('gas resistance', color=color)
        ax2.set_ylim(bottom=0, top=gas.max())
        ax2.plot(time, gas, color=color)

        fig.tight_layout()
        plt.show()
