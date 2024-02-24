# system imports
from time import sleep
import threading

# weight sensor imports
from hx711 import HX711
import RPi.GPIO as GPIO
from gpiozero import LED

# display imports
from nicegui import run, ui, app
import requests
import json

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
CSS_LABEL_SMALL = 'color: #333333; font-variant: small-caps; font-size: medium; font-family: Andale Mono, monospace'

# ui variables and basic settings
#ui_tap1_image = ui.image().style("width: 250px")
#ui_tap1_beer_name = ui.label('CSS').style(CSS_LABEL_SMALL)
#ui_tap1_abv = ui.label('CSS').style(CSS_LABEL_SMALL)
#ui_tap1_ibu = ui.label('CSS').style(CSS_LABEL_SMALL)
#ui_tap2_image = ui.image().style("width: 250px")
#ui_tap2_beer_name = ui.label('CSS').style(CSS_LABEL_SMALL)
#ui_tap2_abv = ui.label('CSS').style(CSS_LABEL_SMALL)
#ui_tap2_ibu = ui.label('CSS').style(CSS_LABEL_SMALL)

# Global variables to communicate between threads
terminate_thread = False
sensor_1_pct = 0
sensor_2_pct = 0

# global variables for web site api calls
tap1_beer_name = ''
tap1_abv = ''
tap1_ibu = ''
tap1_image_url = ''
tap2_beer_name = ''
tap2_abv = ''
tap2_ibu = ''
tap2_image_url = ''


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
		
def get_on_tap_info():
	
	global tap1_beer_name
	global tap1_abv
	global tap1_ibu
	global tap1_image_url
	global tap2_beer_name
	global tap2_abv
	global tap2_ibu
	global tap2_image_url
	
	global terminate_thread
	
	api_key = "IST.eyJraWQiOiJQb3pIX2FDMiIsImFsZyI6IlJTMjU2In0.eyJkYXRhIjoie1wiaWRcIjpcIjI4ODk4OTNjLWEwNTgtNGYyZS1hZTljLWZkOTc4NTAyZTY1YVwiLFwiaWRlbnRpdHlcIjp7XCJ0eXBlXCI6XCJhcHBsaWNhdGlvblwiLFwiaWRcIjpcImUyZWRlNzQ2LTk3NGItNGU5MC05YjViLThlMWFhMTgxOTcxM1wifSxcInRlbmFudFwiOntcInR5cGVcIjpcImFjY291bnRcIixcImlkXCI6XCJkM2E5MjY4YS1hYmNhLTRkMDEtOTg5MC05MmJjM2E5YThmZGZcIn19IiwiaWF0IjoxNzA4NzU2Mjc0fQ.RG1RtK-aujdflcHiLK7NZ8BjkjLrC8nuoDPayCkyZ0QE1ZPXCX3BsngKVEmGh6KOZ_Gb58bQJ-d-PUa9WtAwRf3oi756qWpwg8VhWurfJag795rj7qMdV39mbzEU3jIN_HvxZn-T6Lr0dLYQw1Wc1cUgrTDUovJ3EYkug0P8T7M5KMToRovz-fxRaqphGUY1WkuHWEpVAYu5xyVeKAmMkqdy5F3xoR-8nhSjWswtJvYYO5qKPvPfEW5G1HZCsZEWwnk-tlkU0EbC2v68hzZlJmJ3ChV2h4PfR00Y4ks12WuUinEaOoIxFVi2jM32i-7WDtvsB_TlVHKOhKKrsf7eMQ"

	account_id = "d3a9268a-abca-4d01-9890-92bc3a9a8fdf"
	site_id = "a8995e51-a20f-4a5b-88ca-720ed93eb1a7"

	query_endpoint = 'https://www.wixapis.com/wix-data/v2/items/query'
	image_base_url = 'https://static.wixstatic.com/media/'

	query_data = {
	  "dataCollectionId": "BeerRecipes"
	}

	# define the header
	headers = {
		#'Content-Type': 'application/json',
		'Authorization': f'{api_key}',
		#'wix-account-id': f'{account_id}',
		'wix-site-id': f'{site_id}'  # Example content type
	}

	while not terminate_thread:
	
		response = requests.post(query_endpoint, headers=headers, params=query_data)

		# Check if the request was successful (status code 200)
		if response.status_code == 200:
			# Parse the JSON response
			data = response.json()
			
			element_count = data['pagingMetadata']['count']

			print(f"I found {element_count} elements")
			
			# Access the parsed data (as a Python dictionary)
			num = 0
			while num < element_count:
				
				#find information for Tap 1
				if data['dataItems'][num]['data']['onTap'] == 'Tap1':

					tap1_beer_name = data['dataItems'][num]['data']['title']            
					tap1_abv = data['dataItems'][num]['data']['actualAbv']
					tap1_ibu = data['dataItems'][num]['data']['calculatedIbu']
					
					# get the image string and split the string by "/" and then put the full url together
					parts = data['dataItems'][num]['data']['image'].split("/")
					tap1_image_url = image_base_url + parts[3]
					
					print(tap1_beer_name)
					print(tap1_abv)
					print(tap1_ibu)
					print(tap1_image_url)
					
				if data['dataItems'][num]['data']['onTap'] == 'Tap2':

					#find information for Tap 2
					tap2_beer_name = data['dataItems'][num]['data']['title']            
					tap2_abv = data['dataItems'][num]['data']['actualAbv']
					tap2_ibu = data['dataItems'][num]['data']['calculatedIbu']
					
					# get the image string and split the string by "/" and then put the full url together
					parts = data['dataItems'][num]['data']['image'].split("/")
					tap2_image_url = image_base_url + parts[3]
					
					print(tap2_beer_name)
					print(tap2_abv)
					print(tap2_ibu)
					print(tap2_image_url)
					
				num += 1
				
		else:
			print(f'Error: {response.status_code}')
			
		sleep(15);

def update_ui():

	ui_tap1_image.set_source(tap1_image_url)
	ui_tap1_abv.set_text(f"{tap1_abv} ABV")
	ui_tap1_ibu.set_text(f"{tap1_ibu} IBU")
	ui_tap2_image.set_source(tap2_image_url) 
	ui_tap2_abv.set_text(f"{tap2_abv} ABV") 
	ui_tap2_ibu.set_text(f"{tap2_ibu} IBU") 


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
	
	thread2 = threading.Thread(target=get_on_tap_info)
	thread2.start()
	
	### FIX THIS LATER!!!! (not a good implementation)
	sleep(5)
	
	# setup up the UI for the web page
	with ui.row():
		ui.image('../media/Ostentatious Brewing - Robot 2.jpeg').style("width: 100px")
		ui.link('Ostentatious Brewing', 'https://ostentatiousbrewing.wixsite.com/ostentatiousbrewing', new_tab=True).style(CSS_HEADING_H1)
	ui.label('CSS').style(CSS_HEADING_H2).set_text("This is what is on tap!")
	with ui.row():
		with ui.card():
			ui.label('CSS').style(CSS_HEADING_H2).set_text("Tap 1")
			ui_tap1_image = ui.image(tap1_image_url).style("width: 250px")
			ui_tap1_abv = ui.label('CSS').style(CSS_LABEL_SMALL)
			ui_tap1_ibu = ui.label('CSS').style(CSS_LABEL_SMALL)
			ui_tap1_pct_beer = ui.label('CSS').style(CSS_LABEL)
		with ui.card():
			ui.label('CSS').style(CSS_HEADING_H2).set_text("Tap 2")		
			ui_tap2_image = ui.image(tap2_image_url).style("width: 250px")
			ui_tap2_abv = ui.label('CSS').style(CSS_LABEL_SMALL)
			ui_tap2_ibu = ui.label('CSS').style(CSS_LABEL_SMALL)
			ui_tap2_pct_beer = ui.label('CSS').style(CSS_LABEL)
	
	# update UI elements on a timer
	ui.timer(1.0, lambda: ui_tap1_pct_beer.set_text(f'{sensor_1_pct}% Beer Remaining'))
	ui.timer(1.0, lambda: ui_tap2_pct_beer.set_text(f'{sensor_2_pct}% Beer Remaining'))
	
	### TODO: TURN THIS GARBAGE INTO A PROPER IMPLEMENTATION :) ###
	
	ui.timer(15.0, lambda: update_ui()) 
#	ui.timer(15.0, lambda: ui_tap1_image.set_source(tap1_image_url)) 
#	ui.timer(15.0, lambda: ui_tap1_abv.set_text(f"{tap1_abv} ABV")) 
#	ui.timer(15.0, lambda: ui_tap1_ibu.set_text(f"{tap1_ibu} IBU")) 
#	ui.timer(15.0, lambda: ui_tap2_image.set_source(tap2_image_url)) 
#	ui.timer(15.0, lambda: ui_tap2_abv.set_text(f"{tap2_abv} ABV")) 
#	ui.timer(15.0, lambda: ui_tap2_ibu.set_text(f"{tap2_ibu} IBU")) 
	
	
	# run the UI
	ui.run(reload = False, title="Ostentatious Brewing")
	
	# Wait for keyboard input to terminate the thread
	input("Press Enter to stop the program..\n")
	terminate_thread = True
	thread.join()

	
finally:
	print('Cleaning up the GPIO...')
	GPIO.cleanup()  # always do a GPIO cleanup in your scripts!
	
	
