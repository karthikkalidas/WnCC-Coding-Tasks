import json
import urllib
import requests
from collections import OrderedDict

API_KEY='AIzaSyBJprXQc2vR0lpfAncNWsSBre1Q78JnOEQ'

origin_place='IIT Bombay'

Dist_road=[]
Dist_noroad=[]

with open("input.txt", 'r') as f:
        PlacesList = [line.rstrip('\n') for line in f]

def places_arguement(PlacesList):
	placearg=''
	for places in PlacesList:
		placearg+=places+'|'
	return placearg

def distance_fetch():
	i = 0
	for row in response_json['rows'][0]['elements']:
		#If a road path is found
		if row['status'] == "OK":
			Dist_road.append(
										{
											'location': PlacesList[i], 
											'value': row['distance']['value'],
											'distance': row['distance']['text']
										}
									)

		#If not
		else:
			Dist_noroad.append(PlacesList[i])

		i += 1

def sortit():
	Dist_road.sort()
	sortedList = sorted(Dist_road, key= lambda Dist_road: Dist_road['value'])

	for i in sortedList:
		print(i['location'] + ": " + i['distance'])

	for notFound in Dist_noroad:
		print(notFound + ": No path found")

#PATH-DISTANCE SORTING
print("Sorted using distance by road: ")

reqstparams  = {'origins': origin_place, 'destinations': places_arguement(PlacesList), 'key': API_KEY}

response = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?', params = reqstparams)

response_json  = response.json()

distance_fetch()
sortit()

#BIRD'S LINE DISTANCE SORTING

