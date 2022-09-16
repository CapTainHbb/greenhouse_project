from os import environ
from time import sleep
from ACTUATOR import ACTUATOR
from AHN72 import AHN72
from AHT20 import AHT20
from CAMERA import CAMERA
from COMVIS import COMVIS
from upporting_parameters import *
import datetime
import csv


class MAIN:
    def __init__(self):

        # initializing actuators
        self.fan = ACTUATOR(FAN_GPIO_PIN_NUMBER, GPIO_STATE_HIGH, ACTIVE_LOW_STATE)
        self.heater = ACTUATOR(HEATER_GPIO_PIN_NUMBER, GPIO_STATE_HIGH, ACTIVE_LOW_STATE)
        self.vapor = ACTUATOR(VAPOR_GPIO_PIN_NUMBER, GPIO_STATE_HIGH, ACTIVE_LOW_STATE)
        self.valve = ACTUATOR(VALVE_GPIO_PIN_NUMBER, GPIO_STATE_HIGH, ACTIVE_LOW_STATE)
        self.tomato_grow_stage = 0

        # initializing sensors
        self.air_temp_and_hum_sensor = AHT20()
        # self.soil_hum_sensor = AHN72()
        self.camera = CAMERA(output_photo_dir_name)

        # initializing comptuter vision module
        self.comvis = COMVIS(output_photo_dir_name)
        self.tomato_grow_stage = self.comvis.get_plant_grow_stage()

        # initializing supporting values
        self.current_air_temp = 0
        self.current_air_humidity = 0
        self.current_soil_humidity = 0
        self.measurment_timestamp = 0

        # initializing output file
        with open('environment_parameters.csv', mode='w') as csv_file:
            fieldnames = [AIR_TEMPERATURE, 
                        AIR_HUMIDITY, 
                        SOIL_HUMIDITY, 
                        TOMATO_GROW_STAGE,
                        MEASURMENT_TIMESTAMP]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

    def start(self):
        """
        this is the main funcion of this class.
        """
        while True:
            ### first, sense the enviromental parameters
            self.current_air_temp = self.air_temp_and_hum_sensor.get_temperature()
            self.current_air_humidity = self.air_temp_and_hum_sensor.get_humidity()
            # self.current_soil_humidity = self.soil_hum_sensor.get_humidity()
            self.current_air_humidity = 630
            ct = datetime.datetime.now()
            ts = ct.timestamp()
            self.measurment_timestamp = ct.strftime('%H:%M:%S')

            # write the env parameters value to file
            self.write_environment_parameters_to_file()

            # only take photo at certain time of day
            if ct.hour == TAKE_PHOTO_HOUR and ct.minute == TAKE_PHOTO_MINUTE:
                self.camera.take_photo()
                self.tomato_grow_stage = self.comvis.get_plant_grow_stage()

            ### second, change the enviromental parameters step by step
            ### according to previous step
            if self.tomato_grow_stage >= 1 and self.tomato_grow_stage <=3:
                self.regulate_environment_parameters(self.tomato_grow_stage)
            else:
                print("not supported stage!")
                return OPERATION_FAILED          
            
            sleep(2)

    def stop(self):
        """
        stops all of the actuators
        """
        self.fan.disable()
        self.heater.disable()
        self.valve.disable()
        self.vapor.disable()

    def regulate_environment_parameters(self, grow_stage_number):
        """
           this function regulate the environmental parameters 
           according to  current tomato grow stage.
           note that this function only permits to regulate only one
           parameter at a time!
        """
        rc = self.regulate_air_temperature(grow_stage_number)
        if OPERATION_COMPELETED_SUCESSFULLY != rc:
            return rc
        
        rc = self.regulate_air_humidity(grow_stage_number)
        if OPERATION_COMPELETED_SUCESSFULLY != rc:
            return rc

        rc = self.regulate_soil_humidity(grow_stage_number)
        if OPERATION_COMPELETED_SUCESSFULLY != rc:
            return rc

        return rc

    def regulate_air_temperature(self, grow_stage_number):
        air_temp_lower_bound = 0
        air_temp_upper_bound = 0
        
        if 1 == grow_stage_number:
            air_temp_lower_bound = TOMATO_GROW_STAGE_ONE_AIR_TEMP_LOWER_BOUND
            air_temp_upper_bound = TOMATO_GROW_STAGE_ONE_AIR_TEMP_UPPER_BOUND

        elif 2 == grow_stage_number:
            air_temp_lower_bound = TOMATO_GROW_STAGE_TWO_AIR_TEMP_LOWER_BOUND
            air_temp_upper_bound = TOMATO_GROW_STAGE_TWO_AIR_TEMP_UPPER_BOUND

        elif 3 == grow_stage_number:
            air_temp_lower_bound = TOMATO_GROW_STAGE_THREE_AIR_TEMP_LOWER_BOUND
            air_temp_upper_bound = TOMATO_GROW_STAGE_THREE_AIR_TEMP_UPPER_BOUND

        else:
            print("unsopported stage number in regulate_air_temperature")
            return OPERATION_FAILED

        if self.current_air_temp < air_temp_lower_bound:
                self.heater.enable()
                self.fan.disable() 
                print("------------------regulate temperature--------------------")
                print("current_air_temp#" + str(self.current_air_temp) +
                " < air_temp_lower_bound#" + str(air_temp_lower_bound))
                print("heater enabled, fan disabled")
                print("----------------------------------------------------------")
                return OPERATION_IS_IN_PROCESS


        elif self.current_air_temp > air_temp_upper_bound:
            self.heater.disable()
            self.fan.enable()
            print("------------------regulate temperature--------------------")
            print("current_air_temp#" + str(self.current_air_temp) +
            " > air_temp_lower_bound#" + str(air_temp_lower_bound))
            print("heater disabled, fan enabled")
            print("----------------------------------------------------------")
            return OPERATION_IS_IN_PROCESS
        
        else:
            self.heater.disable()
            self.fan.disable()
            print("------------------regulate temperature--------------------")
            print("current_air_temp#" + str(self.current_air_temp) +
            ",air_temp_lower_bound#" + str(air_temp_lower_bound) + 
            ",air_temp_upper_bound#" + str(air_temp_upper_bound))
            print("heater disabled, fan disabled")
            print("----------------------------------------------------------")
            return OPERATION_COMPELETED_SUCESSFULLY
        
    def regulate_air_humidity(self, grow_stage_number):
        air_hum_lower_bound = 0
        air_hum_upper_bound = 0

        if 1 == grow_stage_number:
            air_hum_lower_bound = TOMATO_GROW_STAGE_ONE_AIR_HUMIDITY_LOWER_BOUND
            air_hum_upper_bound = TOMATO_GROW_STAGE_ONE_AIR_HUMIDITY_UPPER_BOUND

        elif 2 == grow_stage_number:
            air_hum_lower_bound = TOMATO_GROW_STAGE_TWO_AIR_HUMIDITY_LOWER_BOUND
            air_hum_upper_bound = TOMATO_GROW_STAGE_TWO_AIR_HUMIDITY_UPPER_BOUND

        elif 3 == grow_stage_number:
            air_hum_lower_bound = TOMATO_GROW_STAGE_THREE_AIR_HUMIDITY_LOWER_BOUND
            air_hum_upper_bound = TOMATO_GROW_STAGE_THREE_AIR_HUMIDITY_UPPER_BOUND
        
        else:
            print("unsopported stage number in regulate_air_humidity")
            return OPERATION_FAILED

        if self.current_air_humidity < air_hum_lower_bound:
            self.vapor.enable()
            self.fan.disable()
            print("------------------regulate air humidity--------------------")
            print("current_air_humidity#" + str(self.current_air_humidity) +
            " < air_hum_lower_bound#" + str(air_hum_lower_bound))
            print("vapor enabled, fan disabled")
            print("----------------------------------------------------------")
            return OPERATION_IS_IN_PROCESS

        elif self.current_air_humidity > air_hum_upper_bound:
            self.fan.enable()
            self.vapor.disable()
            print("------------------regulate air humidity--------------------")
            print("current_air_humidity#" + str(self.current_air_humidity) +
            " > air_hum_lower_bound#" + str(air_hum_upper_bound))
            print("vapor disabled, fan enabled")
            print("----------------------------------------------------------")
            return OPERATION_IS_IN_PROCESS
        
        else:
            self.vapor.disable()
            self.fan.disable()
            print("------------------regulate air humidity--------------------")
            print("current_air_humidity#" + str(self.current_air_humidity) +
            ", air_hum_lower_bound#" + str(air_hum_lower_bound) +
            ", air_hum_upper_bound#" + str(air_hum_upper_bound)
            )
            print("vapor disabled, fan disabled")
            print("----------------------------------------------------------")
            return OPERATION_COMPELETED_SUCESSFULLY

    # to do: invalid lower and upper bound
    def regulate_soil_humidity(self, grow_stage_number):
        soil_hum_lower_bound = 0
        soil_hum_upper_bound = 0

        if 1 == grow_stage_number:
            soil_hum_lower_bound = TOMATO_GROW_STAGE_ONE_SOIL_HUMIDITY_LOWER_BOUND
            soil_hum_upper_bound = TOMATO_GROW_STAGE_ONE_SOIL_HUMIDITY_UPPER_BOUND

        elif 2 == grow_stage_number:
            soil_hum_lower_bound = TOMATO_GROW_STAGE_TWO_SOIL_HUMIDITY_LOWER_BOUND
            soil_hum_upper_bound = TOMATO_GROW_STAGE_TWO_SOIL_HUMIDITY_UPPER_BOUND

        elif 3 == grow_stage_number:
            soil_hum_lower_bound = TOMATO_GROW_STAGE_THREE_SOIL_HUMIDITY_LOWER_BOUND
            soil_hum_upper_bound = TOMATO_GROW_STAGE_THREE_SOIL_HUMIDITY_UPPER_BOUND
        
        else:
            print("unsopported stage number in regulate_air_humidity")
            return OPERATION_FAILED

        if self.current_soil_humidity < soil_hum_lower_bound:
            self.valve.enable()
            print("-----------------regulate soil humidity-----------------")
            print("current_air_temp#" + str(self.current_soil_humidity) +
            " < soil_hum_lower_bound#" + str(soil_hum_lower_bound))
            print("valve enabled")
            print("--------------------------------------------------------")
        elif self.current_soil_humidity > soil_hum_upper_bound:
            self.valve.disable()
            print("-----------------regulate soil humidity-----------------")
            print("current_air_temp#" + str(self.current_soil_humidity) +
            " > soil_hum_upper_bound#" + str(soil_hum_upper_bound))
            print("valve disabled")
            print("--------------------------------------------------------")
        else:
            self.valve.disable()
            print("-----------------regulate soil humidity-----------------")
            print("current_air_temp#" + str(self.current_soil_humidity) +
            ",soil_hum_lower_bound#" + str(soil_hum_lower_bound) +
            ",soil_hum_upper_bound#" + str(soil_hum_upper_bound))
            print("valve disabled")
            print("--------------------------------------------------------")
            

    def get_environment_parameters_dict(self):
        env_par_dict = {}
        env_par_dict[AIR_TEMPERATURE] = self.current_air_temp
        env_par_dict[AIR_HUMIDITY] = self.current_air_humidity
        env_par_dict[SOIL_HUMIDITY] = self.current_soil_humidity
        env_par_dict[TOMATO_GROW_STAGE] = self.tomato_grow_stage
        env_par_dict[MEASURMENT_TIMESTAMP] = self.measurment_timestamp
        return env_par_dict

    def write_environment_parameters_to_file(self):
        environment_parameters = self.get_environment_parameters_dict()
        with open(OUTPUT_CSV_FILENAME, mode='a') as csv_file:
            fieldnames = environment_parameters.keys()
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow(environment_parameters)

