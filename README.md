# greenhouse_project
This is an awsome automation system for greenhouses!
this automation system desinged for tomato!

compenents of this greenhouse:

1) sensors: 
   * AHT20 -> for air temperature and humidity
   * AHN72 -> for soil humidity
   * raspberry pi camera -> to capture images for processing

2) acutators:
  * valve
  * fan
  * heater
  * humidifier

3) modules:
  * computer vision module: this module uses images capatured by rapberry pi camera to determine
    grow stage of plant. to determine grow stage of plant, the YOLOV5 algorithm is used.
  
  * main module: this module gathers data from sensors and takes action through actuators based on grow stage of plant
  
  * ui : this module show statistical information to user by matplotlib
