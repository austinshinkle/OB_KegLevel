# system imports
from time import sleep
import threading

# weight sensor imports
from hx711 import HX711
import RPi.GPIO as GPIO
from gpiozero import LED

# display imports
from nicegui import run, ui, app

# samples that should be taken for each sensor
SAMPLES = 5

# calibration data for sensor 1
SENSOR_1_OFFSET = -519856.2 #temp value
SENSOR_1_SCALE = 1/1000 #temp value

# calibration data for sensor 2
SENSOR_2_OFFSET = -640729.2 #temp value
SENSOR_2_SCALE = 1/600 #temp value

# styles for CSS formatting
CSS_HEADING_H1 = 'color: #111111; font-variant: small-caps; font-size: xxx-large; font-weight: 500; font-family: Andale Mono, monospace'
CSS_HEADING_H2 = 'color: #222222; font-variant: small-caps; font-size: xx-large; font-weight: 500; font-family: Andale Mono, monospace'
CSS_LABEL = 'color: #333333; font-variant: small-caps; font-size: x-large; font-family: Andale Mono, monospace'

# on tap images
ON_TAP_KEG_1_IMAGE = 'https://static.wixstatic.com/media/22ae94_0e87a582058c47d1ba8227377bd4b334~mv2.png'
ON_TAP_KEG_2_IMAGE = 'https://static.wixstatic.com/media/d3a926_41fdde2b7fce45c8a37755d2797470c3~mv2.png'

# Global variables to communicate between threads
terminate_thread = False
sensor_1_pct = 0
sensor_2_pct = 0


led_green = LED(12)
led_red = LED(25)

def measure_kegs():
	
	global terminate_thread
	global sensor_1_pct
	global sensor_2_pct
	
	while not terminate_thread:
		
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
		#print(f"{sensor_1_pct}%,{sensor_2_pct}%")

		sleep(.5)


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

	# start the thread to measure the kegs
	thread = threading.Thread(target=measure_kegs)
	thread.start()
	
	### FIX THIS LATER!!!! (not a good implementation)
	sleep(5)
	
	# setup up the UI for the web page
	with ui.row():
		ui.image('../media/Ostentatious Brewing - Robot 2.jpeg').style("width: 100px")
		ui.label('CSS').style(CSS_HEADING_H1).set_text("Ostententatious Brewing!")
	ui.label('CSS').style(CSS_HEADING_H2).set_text("This is what is on tap!")
	with ui.row():
		with ui.card():
			ui.label('CSS').style(CSS_HEADING_H2).set_text("Tap 1")
			ui.image(ON_TAP_KEG_1_IMAGE).style("width: 250px")
			keg_1 = ui.label('CSS').style(CSS_LABEL)
		with ui.card():
			ui.label('CSS').style(CSS_HEADING_H2).set_text("Tap 2")		
			ui.image(ON_TAP_KEG_2_IMAGE).style("width: 250px")
			keg_2 = ui.label('CSS').style(CSS_LABEL)
	ui.link('Ostentatious Brewing Website', 'https://ostentatiousbrewing.wixsite.com/ostentatiousbrewing', new_tab=True).style(CSS_LABEL)
	
	# update UI elements on a timer
	ui.timer(1.0, lambda: keg_1.set_text(f'{sensor_1_pct}% Beer Remaining'))
	ui.timer(1.0, lambda: keg_2.set_text(f'{sensor_2_pct}% Beer Remaining'))
	
	# run the UI
	ui.run(reload=False, title="Ostentatious Brewing")
	
	# Wait for keyboard input to terminate the thread
	input("Press Enter to stop the program..\n")
	terminate_thread = True
	thread.join()

	
finally:
	print('Cleaning up the GPIO...')
	GPIO.cleanup()  # always do a GPIO cleanup in your scripts!
	
	
