from hx711 import HX711
import RPi.GPIO as GPIO
from time import sleep

try:
	
	while True:

		try:
			hx711 = HX711(
				dout_pin=5,
				pd_sck_pin=6,
				channel='A',
				gain=128
			)

			hx711.reset()   # Before we start, reset the HX711 (not obligate)
			measures = hx711.get_raw_data(times=5)
		finally:
			GPIO.cleanup()  # always do a GPIO cleanup in your scripts!

		print(measures)
    
		sleep(1)
	
	
except KeyboardInterrupt:
	print('Script cancelled by user!')
