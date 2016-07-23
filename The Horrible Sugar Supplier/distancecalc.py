import json
import urllib
API_KEY='AIzaSyBJprXQc2vR0lpfAncNWsSBre1Q78JnOEQ'

with open("input.txt", 'r') as f:
        PlacesList = [line.rstrip('\n') for line in f]

urlstring='+'.join(PlacesList)
print(urlstring)


