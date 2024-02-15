from hx711 import HX711
import RPi.GPIO as GPIO
from time import sleep
from gpiozero import LED

# samples that should be taken for each sensor
SAMPLES = 5

OFFSET_SCALE_1 = -519856.2
OFFSET_SCALE_2 = -640729.2

led_green = LED(12)
led_red = LED(25)

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
			
			# apply offset
			sensor_1_avg = int(sensor_1_avg - OFFSET_SCALE_1)
			
			
						
			measures_2 = hx711_2.get_raw_data(times=SAMPLES)
			
			num = 0
			while num < SAMPLES:
				sensor_2_avg += measures_2[num]
				num += 1
			sensor_2_avg /= SAMPLES
			
			# apply offset
			sensor_2_avg = int(sensor_2_avg - OFFSET_SCALE_2)
			
			if sensor_1_avg < 0:
				led_red.on();
				led_green.off()
			else:
				led_red.off();
				led_green.on()	
			

			print(f"{sensor_1_avg},{sensor_2_avg}")
    
			sleep(.5)
		
		# add a GPIO exception here
		except KeyboardInterrupt:
			print('Script cancelled by user!')
			print('Cleaning up the GPIO...')
			GPIO.cleanup()  # always do a GPIO cleanup in your scripts!
			break
		

	
except KeyboardInterrupt:
	print('Script cancelled by user!')
	print('Cleaning up the GPIO...')
	GPIO.cleanup()  # always do a GPIO cleanup in your scripts!
	
	
