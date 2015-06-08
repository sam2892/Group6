import requests 
import json
import time


f = open('dudewhereis.html','w')
message = "<html><head><meta http-equiv=\"refresh\" content=\"5\" /></head><body>No alerts</body></html>"
f.write(message)
f.close()


oldX = ''
oldY = ''


# Call the MAC OUI check API
OUIURL = 'http://www.macvendorlookup.com/api/v2/88:53:95:73:d4:c1'
responseOUI = requests.get(OUIURL)
myrespOUI = responseOUI.json()


header = {'Accept':'Application/JSON'}
url = 'https://10.1.1.21//api/contextaware/v1/location/clients/88:53:95:73:d4:c1'

# this statement performs a GET on the specified url
response = requests.get(url,verify=False,auth=('hackathon','hackathon'),headers=header)

# print the json that is returned
#print response.json()
#print response.headers['Content-Type']

myresp = response.json()

oldX = myresp["WirelessClientLocation"]["MapCoordinate"]["x"]
oldY = myresp["WirelessClientLocation"]["MapCoordinate"]["y"]

newX = oldX
newY = oldY

timer = 0

while (newX - oldX < 1) and (newY - oldY < 1):

	response = requests.get(url,verify=False,auth=('hackathon','hackathon'),headers=header)
	myresp = response.json()
	newX = myresp["WirelessClientLocation"]["MapCoordinate"]["x"]
	newY = myresp["WirelessClientLocation"]["MapCoordinate"]["y"]
	time.sleep(5)
	timer = timer + 5
	print "\n\nTime:", timer, "Coordinates: NEW:", newX, newY, "OLD:", oldX, oldY
	print ""
	print ""

mac = myresp["WirelessClientLocation"]["macAddress"]
vendor = myrespOUI[0]["company"]

print "Client MAC Address is:\t", myresp["WirelessClientLocation"]["macAddress"]
print "Vendor of client:\t", myrespOUI[0]["company"]
print ""
print "\tOLD Location\tNEW Location"
print "X:\t", oldX, "\t\t", newX
print "Y:\t", oldY, "\t\t", oldY


f = open('dudewhereis.html','w')

message = "<html><head><meta http-equiv=\"refresh\" content=\"5\" /></head><body><p> <h1>ALERT</h1><p>"

z = "Client with MAC Address <b> %s </b> has moved. Vendoris <b> %s" % (mac,vendor)
message = message + z

z = "<p>OLD Location: X: %s and Y: %s" % (oldX,oldY) 

message = message + z
z = "<br>NEW Location: X: %s and Y: %s" % (newX,newY)

message = message + z

tail = "</p></body></html>"
message = message + tail

f.write(message)
f.close()

