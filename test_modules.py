from modules.AHT20 import AHT20
from modules.CAMERA import CAMERA
from modules.COMVIS import COMVIS
from modules.supporting_parameters import *
from time import sleep
from modules.ACTUATOR import ACTUATOR

def test_temperature_module():
    air_temp_and_hum_sensor = AHT20()

    while True:
        sleep(2)
        print(str(air_temp_and_hum_sensor.get_humidity()) + " %")
        print(str(air_temp_and_hum_sensor.get_temperature()) + " C")

def test_comvis():
    comvis_obj = COMVIS(output_photo_dir_name)
    comvis_obj.get_latest_photo()

def test_fan():
    fan_obj = ACTUATOR(FAN_GPIO_PIN_NUMBER, GPIO_STATE_HIGH, ACTIVE_LOW_STATE)
    fan_obj.disable()
    sleep(10)
    fan_obj.enable()


def test_vapor():
    fan_obj = ACTUATOR(VAPOR_GPIO_PIN_NUMBER, GPIO_STATE_HIGH, ACTIVE_LOW_STATE)
    fan_obj.disable()
    sleep(30)
    fan_obj.enable()

test_temperature_module()