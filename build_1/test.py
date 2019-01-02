### 
### Daniel Ryaboshapka
### Friday, December 21st 2018
### test.py -- Prototype Work for the AirTraffic Finder application. 
### Updated January 2019
### 

## RESOURCES: https://developers.google.com/public-data/docs/canonical/countries_csv for countries.csv
## https://data.humdata.org/dataset/bounding-boxes-for-countries for bounding boxes for country_boundingboxes.csv
## https://en.wikipedia.org/wiki/Haversine_formula for Haversine formula used to calculate distances
## https://en.wikipedia.org/wiki/Vincenty%27s_formulae will use Vincenty formula in later iterations for better accuracy
## https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
## 	  ^ learned how to use map function to convert decimal latitude and longitude to radians

#Import Statements 
from opensky_api import OpenSkyApi
from collections import defaultdict
from countries import country_dict
from math import radians, sin, asin, cos, sqrt
import csv

# Test Run of everything
# api = OpenSkyApi()
# states = api.get_states()
# for s in states.states:
#     print("(%r, %r, %r, %r, %r degrees, %r meters)" % (s.callsign, s.origin_country, \
#     	s.longitude, s.latitude, s.heading, s.geo_altitude))


# setting global variables
program_life = True
curr_planes = list()
curr_country = ""
print("Fetching data...")
api = OpenSkyApi()
states = api.get_states()

# # Read in data from country_latitude_longitude.csv and form a Dictionary
# csv_reader = csv.reader(open('country_latitude_longitude.csv', 'r'))
# for line in csv_reader:
# 	for x in range(1,4):
# 		country_dict[line[0]].append(line[x])


# Current list of functions 
# Using a dictionary to map the strings of the commands to the respective functions
def input_switch(arg):
	switch = {
		"country": country,
		"callsign": callsign,
		"list": listall,
		"distance": distance,
		"clear": clearlist,
		"q": quit
	}
	func = switch.get(arg, lambda: "Invalid input")
	
	try:
		func(arg)
	except TypeError:
		print("Invalid Input, please try again.")
		userInput = input("Select Query: ")		
		input_switch(userInput)


def update_states():
	print("Fetching data...")
	states = api.get_states()

def fix_bounding_boxes(bounding_box, states):
	if bounding_box[1][2] < bounding_box[1][0]:
		if bounding_box[1][1] < bounding_box[1][3]:
			states = api.get_states(bbox = (bounding_box[1][1], bounding_box[1][3], bounding_box[1][2], bounding_box[1][0]))
			print(bounding_box[1][1], bounding_box[1][3], bounding_box[1][2], bounding_box[1][0], "\n")
		else:
			states = api.get_states(bbox = (bounding_box[1][3], bounding_box[1][1], bounding_box[1][2], bounding_box[1][0]))
			print(bounding_box[1][3], bounding_box[1][1], bounding_box[1][2], bounding_box[1][0], "\n")
	else: 
		if bounding_box[1][1] < bounding_box[1][3]:
				states = api.get_states(bbox = (bounding_box[1][1], bounding_box[1][3], bounding_box[1][0], bounding_box[1][2]))
				print(bounding_box[1][1], bounding_box[1][3], bounding_box[1][0], bounding_box[1][2], "\n")
		else:
			states = api.get_states(bbox = (bounding_box[1][3], bounding_box[1][1], bounding_box[1][0], bounding_box[1][2]))
			print(bounding_box[1][3], bounding_box[1][1], bounding_box[1][0], bounding_box[1][2], "\n")
	return states

def distance(arg):
	global api
	global states
	global curr_planes

	plane_list = list()

	#Gather plane data
	print("Do you want to find planes from your list or search two planes by callsign?")
	pref = input("Enter <list> or <callsign> to choose: ")

	if pref == "list":
		listall(arg)
		plane1 = input("Select the index of the plane in your list: ")
		plane2 = input("Select another index: ")
		plane1 = int(plane1)
		plane2 = int(plane2)
		plane_list.append(curr_planes[plane1])
		plane_list.append(curr_planes[plane2])

	if pref == "callsign":
		state_plane1 = modified_callsign()
		state_plane2 = modified_callsign()
		plane_list.append(state_plane1)
		plane_list.append(state_plane2)

	if pref != "callsign" and pref != "list":
		print("Invalid Input. Please try again")
		distance(arg)

	#Calculate distance with Haversine formula
	#Since Earth isn't a perfect sphere, the distance calculated will have an error of 
	#around .5% (quoted from Haversine Formula (wikipedia, link under resources))
	earthrad = 6371.393 # in km 
	lat1 = plane_list[0].latitude
	long1 = plane_list[0].longitude
	alt1 = plane_list[0].geo_altitude
	lat2 = plane_list[1].latitude
	long2 = plane_list[1].longitude
	alt2 = plane_list[1].geo_altitude

	lat1, long1, lat2, long2 = map(radians, [lat1, long1, lat2, long2])

	inner1 = sin((lat2 - lat1)/2)**2
	inner2 = cos(lat1) * cos(lat2) * sin((long2 - long1)/2)**2
	added = inner1 + inner2
	d = 2 * earthrad * asin(sqrt(added))
	dmiles = d * .621371

	#incorporate altitude as well
	altitude = abs(alt1 - alt2) / 1000 # for km
	modded_dist = sqrt(altitude**2 + d**2)
	modmiles = modded_dist * .621371

	print("Distance is %f km, or %f miles" % (d, dmiles))
	print("Incorporating altitude, distance is %f km, or %f miles\n" % (modded_dist, modmiles))
	plane_list.clear()

def modified_callsign():
	global states
	global api
	newInput = input("Please enter the EXACT callsign for distance calculation: ")

	if newInput == '':
		print("Not a valid callsign. Please try again.")
		modified_callsign(arg)

	check = 0
	for s in states.states: 
		if newInput in s.callsign:
			print("Plane information:")
			print("(%r, %r, %r, %r, %r degrees, %r meters)\n" % (s.callsign, s.origin_country,\
	    s.longitude, s.latitude, s.heading, s.geo_altitude))
			check += 1
			return s

	if check == 0:
		check_again = input("This plane was not found. Try again? (y) or (yes): ")
		if check_again == "y" or check_again == "yes":
			modified_callsign()

def clearlist(arg):
	print("Clearing list...\n")
	curr_planes.clear()

def country(arg):
	global curr_country
	global states
	global api
	userInput = input("Select the Country: ")
	true_input = False
	index = 0

	while true_input == False:
		if userInput in country_dict:
			curr_country = userInput
			true_input = True
		else:
			print("This country doesn't exist in our records. Please try again.")
			userInput = input("Select the Country: ")


	counter = 0
	if states != None:
		for s in states.states:
			if curr_country in s.origin_country:
				print("(%r, %r, %r, %r, %r degrees, %r meters)" % (s.callsign, s.origin_country, \
	    	s.longitude, s.latitude, s.heading, s.geo_altitude))
				counter += 1

	if counter == 0:
		print("No current flights exist from this country ")

	userInput = input("Check to see if any flights flying over this country? (y) or (yes) ")
	if userInput == "y" or userInput == "yes":
		bounding_box = country_dict[curr_country]
		print("Using Bounding Box of", curr_country)
		
		fix_bounding_boxes(bounding_box, states) #Bounding boxes from dictionary aren't in the 
												 #correct order for the opensky bbox call

		if states != None:
			for s in states.states:
				print("(%r, %r, %r, %r, %r degrees, %r meters)" % (s.callsign, s.origin_country, \
	    	s.longitude, s.latitude, s.heading, s.geo_altitude))
		else:
			print("Could not fetch data. Returning to main screen...")


	update_states()


def callsign(arg): 
	global states
	global api
	newInput = input("Please enter the EXACT callsign of the plane you wish to track: ")

	if newInput == '':
		print("Not a valid callsign. Please try again.")
		callsign(arg)

	for s in curr_planes:
		if newInput in s.callsign:
			print("You already added this plane. Try another callsign")
			callsign(arg)

	check = 0
	for s in states.states: 
		if newInput in s.callsign:
			print("Adding %r to your list...\n" % s.callsign)
			print("Plane information:")
			print("(%r, %r, %r, %r, %r degrees, %r meters)\n" % (s.callsign, s.origin_country,\
	    s.longitude, s.latitude, s.heading, s.geo_altitude))
			curr_planes.append(s)
			check += 1

	if check == 0:
		check_again = input("This plane was not found. Try again? (y) or (yes): ")
		if check_again == "y" or check_again == "yes":
			callsign(arg)

	update_states()

def listall(arg):
	print()

	if len(curr_planes) == 0:
		print("You currently aren't tracking any planes. Use <callsign> to add planes.\n")
		return

	print("Your current tracked planes are:")
	count = -1
	for s in curr_planes:
		count += 1
		print("%d. (%r, %r, %r, %r, %r degrees, %r meters)" % (count, s.callsign, s.origin_country,\
	s.longitude, s.latitude, s.heading, s.geo_altitude))
	print()

def quit(arg):
	global program_life 
	program_life = False
	print("Exiting...")

# Main 
def main(): 
	global program_life 
	global curr_country
	print("Welcome to AirFinder powered by OpenSky API. This program will let you track and calculate current data of all airplanes in the sky.")

	while program_life:
		print("Usage:\n<country>: Select what country you want to narrow your focus down to\n\
<callsign>: Append the plane with given callsign to your Airplane List\n\
<list>: List all current airplanes you are tracking\n\
<distance>: Calculate the distance between two planes\n\
<clear>: clears all tracked data\n\
More usages will follow")

		userInput = input("Select Query: ")
		input_switch(userInput)

if __name__ == '__main__':
	main()