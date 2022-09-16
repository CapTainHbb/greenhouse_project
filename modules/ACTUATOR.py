import RPi.GPIO as GPIO            # import RPi.GPIO module  

class ACTUATOR:
    
    def __init__(self, pin_number, default_output_state=0, active_state="active_low"):
        self.pin_number = pin_number
        GPIO.setmode(GPIO.BCM)                          # choose BCM or BOARD  
        GPIO.setup(self.pin_number, GPIO.OUT)           # set GPIO as an output 
        self.defualt_output_state = default_output_state
        self.active_state = active_state


        if self.defualt_output_state != 0 and self.defualt_output_state != 1:
            self.defualt_output_state = 0
        
        if self.defualt_output_state != "active_low" and self.defualt_output_state != "active_high":
            self.defualt_output_state = "active_low"

        GPIO.output(self.pin_number, default_output_state)

    def enable(self):
        if self.defualt_output_state == "active_low":
            GPIO.output(self.pin_number, 0) 
        else:
            GPIO.output(self.pin_number, 1)

    def disable(self):
        if self.defualt_output_state == "active_low":
            GPIO.output(self.pin_number, 1) 
        else:
            GPIO.output(self.pin_number, 0) 
           
    # Calling destructor
    def __del__(self):
        GPIO.cleanup() 