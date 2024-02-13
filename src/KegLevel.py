from hx711 import HX711
import RPi.GPIO as GPIO
from time import sleep

# samples that should be taken for each sensor
SAMPLES = 5

try:
	
	# channel A for amplifier board @ 128 gain for maximum signal swing
	hx711 = HX711(
		dout_pin=5,
		pd_sck_pin=6,
		channel='A',
		gain=128
	)			
	
	# channel A for amplifier board @ 128 gain maximum signal swing
	hx711_2 = HX711(
		dout_pin=9,
		pd_sck_pin=10,
		channel='A',
		gain=128
	)
	
	# reset the devices
	hx711.reset()   # Before we start, reset the HX711 (not obligate)	
	hx711_2.reset()   # Before we start, reset the HX711 (not obligate)

	
	while True:

		try:
			
			sensor_1_avg = 0
			sensor_2_avg = 0
			
			measures = hx711.get_raw_data(times=SAMPLES)
			
			num = 0
			while num < SAMPLES:
				sensor_1_avg += measures[num]
				num += 1
			sensor_1_avg /= SAMPLES
			
			#print(measures)
			#print(f"The average of sensor 1 = {sensor_1_avg}\n")
			
			measures_2 = hx711_2.get_raw_data(times=SAMPLES)
			
			num = 0
			while num < SAMPLES:
				sensor_2_avg += measures_2[num]
				num += 1
			sensor_2_avg /= SAMPLES
			
			#print(measures_2)
			#print(f"The average of sensor 2 = {sensor_2_avg}\n")

			print(f"{sensor_1_avg},{sensor_2_avg}")
    
			sleep(1)
		
		# add a GPIO exception here
		except:
			pass
		

	
except KeyboardInterrupt:
	print('Script cancelled by user!')
	print('Cleaning up the GPIO...')
	GPIO.cleanup()  # always do a GPIO cleanup in your scripts!
	
	
