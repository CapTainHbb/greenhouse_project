import csv
import matplotlib.pyplot as plt
import numpy as np
from supporting_parameters import *

class UI:
    def __init__(self):
        pass

    def show_graph(self):
        x_points = np.array([])
        air_temp_y_points = np.array([])
        air_hum_y_points = np.array([])
        soil_hum_y_points = np.array([])

        with open(OUTPUT_CSV_FILENAME, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count == 0: # first line is header line
                    line_count += 1
                    continue
                x_points = np.append(x_points, row[MEASURMENT_TIMESTAMP])
                air_temp_y_points = np.append(air_temp_y_points, int(row[AIR_TEMPERATURE]))
                air_hum_y_points = np.append(air_hum_y_points, int(row[AIR_HUMIDITY]))
                soil_hum_y_points = np.append(soil_hum_y_points, int(row[SOIL_HUMIDITY]))       
                line_count += 1 
        
        print(x_points)
        print(air_temp_y_points)
        print(air_temp_y_points)
        print(soil_hum_y_points)

        # plot air temperature
        plt.subplot(3, 1, 1)
        plt.plot(x_points, air_temp_y_points, label="air temperature", color="red")
        plt.legend(loc="upper right")
        plt.xlabel("timestamp")
        plt.ylabel("air temperature in celcius")

        # plot air humidity
        plt.subplot(3, 1, 2)
        plt.plot(x_points, air_hum_y_points, label="air humidity percentage", color="black")
        plt.legend(loc="upper right")
        plt.xlabel("timestamp")
        plt.ylabel("air humidity in percentage")


        # plot soil humidity
        plt.subplot(3, 1, 3)
        plt.plot(x_points, soil_hum_y_points, label="soil humidity resistance", color="blue")
        plt.legend(loc="upper right")
        plt.xlabel("timestamp")
        plt.ylabel("soil humidity resostance value")


        plt.show()