# system imports
from time import sleep

# weight sensor imports
from hx711 import HX711
import RPi.GPIO as GPIO
from gpiozero import LED

# display imports
import justpy as jp

# samples that should be taken for each sensor
SAMPLES = 5

# calibration data for sensor 1
SENSOR_1_OFFSET = -519856.2 #temp value
SENSOR_1_SCALE = 1/1000 #temp value

# calibration data for sensor 2
SENSOR_2_OFFSET = -640729.2 #temp value
SENSOR_2_SCALE = 1/600 #temp value

led_green = LED(12)
led_red = LED(25)

def hello_world():
    wp = jp.WebPage()
    jp.Hello(a=wp)
    return wp

try:
	
	#jp.justpy(hello_world)
	
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

	# main program loop
	while True:

		try:		
			
			### sensor 1 ###
			
			# measure sensor values
			sensor_1_measures = hx711.get_raw_data(times=SAMPLES)
			
			# get average of all sensor values
			sensor_1_raw = 0
			for x in range(SAMPLES):
				sensor_1_raw += sensor_1_measures[x]
				x += 1
			sensor_1_raw /= SAMPLES
			
			# apply scale and offset --> percent
			sensor_1_pct = int(SENSOR_1_SCALE * (sensor_1_raw - SENSOR_1_OFFSET))
			if sensor_1_pct < 0:
				sensor_1_pct = 0
				
			### end sensor 1 ###
			
			### sensor 2 ###	
			
			# measure sensor values
			sensor_2_measures = hx711_2.get_raw_data(times=SAMPLES)
			
			# get average of all sensor values
			sensor_2_raw = 0
			for x in range(SAMPLES):
				sensor_2_raw += sensor_2_measures[x]
				x += 1
			sensor_2_raw /= SAMPLES
			
			# apply scale and offset --> percent
			sensor_2_pct = int(SENSOR_2_SCALE * (sensor_2_raw - SENSOR_2_OFFSET))
			if sensor_2_pct < 0:
				sensor_2_pct = 0
			
			### end sensor 2 ###
			
			# for fun turn on an LED when scale 1 is less than 50
			if sensor_1_pct < 50:
				led_red.on();
				led_green.off()
			else:
				led_red.off();
				led_green.on()	
			
			# show the sensor values
			print(f"{sensor_1_pct}%,{sensor_2_pct}%")
    
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
	
	
