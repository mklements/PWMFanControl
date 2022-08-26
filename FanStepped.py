# Created by: Michael Klements
# For 40mm 5V PWM Fan Control On A Raspberry Pi
# Sets fan speed in stepped increments - better for low quality fans
# Works well with a Pi Desktop Case with OLED Stats Display
# Installation & Setup Instructions - https://www.the-diy-life.com/connecting-a-pwm-fan-to-a-raspberry-pi/

import RPi.GPIO as IO          # Calling GPIO to allow use of the GPIO pins
import time                    # Calling time to allow delays to be used
import subprocess              # Calling subprocess to get the CPU temperature

IO.setwarnings(False)          # Do not show any GPIO warnings
IO.setmode (IO.BCM)            # BCM pin numbers - PIN8 as ‘GPIO14’
IO.setup(14,IO.OUT)            # Initialize GPIO14 as our fan output pin
fan = IO.PWM(14,100)           # Set GPIO14 as a PWM output, with 100Hz frequency (this should match your fans specified PWM frequency)
fan.start(0)                   # Generate a PWM signal with a 0% duty cycle (fan off)

def get_temp():                              # Function to read in the CPU temperature and return it as a float in degrees celcius
    output = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True)
    temp_str = output.stdout.decode()
    try:
        return float(temp_str.split('=')[1].split('\'')[0])
    except (IndexError, ValueError):
        raise RuntimeError('Could not get temperature')

while 1:                                     # Execute loop forever
    temp = get_temp()                        # Get the current CPU temperature
    if temp > 70:                            # Check temperature threshhold, in degrees celcius
        fan.ChangeDutyCycle(100)             # Set fan duty based on temperature, 100 is max speed and 0 is min speed or off.
    elif temp > 60:
        fan.ChangeDutyCycle(85)
    elif temp > 50:
        fan.ChangeDutyCycle(70)
    elif temp > 40:
        fan.ChangeDutyCycle(50)
    elif temp > 32:
        fan.ChangeDutyCycle(25)
    elif temp > 25:
        fan.ChangeDutyCycle(15)
    else:
        fan.ChangeDutyCycle(0)
    time.sleep(5)                            # Sleep for 5 seconds
