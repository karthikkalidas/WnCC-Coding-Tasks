import json
import urllib
import requests
import geopy.distance
import os

API_KEY='AIzaSyBJprXQc2vR0lpfAncNWsSBre1Q78JnOEQ'

origin_place='IIT Bombay'

Dist_road=[]
Dist_noroad=[]
bird_dist=[]
bird_nodist=[]
lat_long = []

with open("input.txt", 'r') as f:
        PlacesList = [line.rstrip('\n') for line in f]

#TO PASS THE PLACES
def places_arguement(PlacesList):
	placearg=''

	for places in PlacesList:
		placearg+=places+'|'

	return placearg

#DISTANCE FETCHING FROM API
def distance_fetch():
	
	reqstparams  = {'origins': origin_place, 'destinations': places_arguement(PlacesList), 'key': API_KEY}

	response = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?', params = reqstparams)

	response_json  = response.json()

	i = 0

	for row in response_json['rows'][0]['elements']:
		#ROAD PATH EXISTS
		if row['status'] == "OK":
			Dist_road.append(
										{
											'location': PlacesList[i], 
											'value': row['distance']['value'],
											'distance': row['distance']['text']
										}
									)

		#ROAD PATH DOES NOT EXIST
		else:
			Dist_noroad.append(PlacesList[i])

		i += 1

#DISTANCE LIST SORTING
def sortdist():
	Dist_road.sort()
	sortedList = sorted(Dist_road, key= lambda Dist_road: Dist_road['value'])

	for place in sortedList:
		print place['location'] + ": " + place['distance']

	for noplace in Dist_noroad:
		print noplace + ": No path found"

#FETCHING THE LATITUDE & LONGITUDE OF A PLACE
def latlongfetch(location):

	reqstparams  = {'address': location}

	response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?', params = reqstparams)

	response_json  = response.json()

	if response_json['status'] == "OK":
		latitude = response_json['results'][0]['geometry']['location']['lat']
		longitude = response_json['results'][0]['geometry']['location']['lng']

		return latitude, longitude
	
	else:
		return "no", "no"

#TO CALCULATE THE GREAT CIRCLE DISTANCE FROM ORIGIN
def circledist(lat_long):
	IITB_latlong = latlongfetch("IIT Bombay")

	return (geopy.distance.vincenty(IITB_latlong, lat_long).meters)/1000

#TO FETCH THE BIRD'S LINE DISTANCE
def birddistfetch():
	i = 0

	for place in PlacesList:
		latitude, longitude =  latlongfetch(place)
		#if valid latitude is there
		if latitude != "no":
			bird_dist.append(
										{
											'value': circledist((latitude, longitude)),
											'location': PlacesList[i]
										}
									)
		else: 
			bird_nodist.append(PlacesList[i])

		i += 1

#BIRD'S LINE DISTANCE LIST SORTING
def sortbirddist():

	bird_dist.sort()
	sortedList = sorted(bird_dist, key= lambda bird_dist: bird_dist['value'])

	for i in sortedList:
		print i['location'] + ": " + str(i['value']) + " km"
		
	for notFound in bird_nodist:
		print notFound + ": No path found" 

##########################################################################################################

#PATH-DISTANCE
os.system('clear')
print "Distance by Road: \n"
distance_fetch()
sortdist()

##########################################################################################################

#BIRD'S-LINE DISTANCE
print "\n"
print "Bird's Line Distance: \n"
birddistfetch()
sortbirddist()