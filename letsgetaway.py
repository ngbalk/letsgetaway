import requests, json
from operator import itemgetter

class Destination:
	def __init__(self, originCity, cityName, countryName, shortName, kayakUrl, departDate, returnDate, airline, price):
		self.originCity = originCity
		self.cityName = cityName
		self.countryName = countryName
		self.shortName = shortName
		self.kayakUrl = 'https://www.kayak.com'+kayakUrl
		self.departDate = departDate
		self.returnDate = returnDate
		self.airline = airline
		self.price = price
	def toString(self):
		return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.originCity, self.cityName, self.countryName, self.shortName, self.kayakUrl, self.departDate, self.returnDate, self.airline, self.price)

def commonDestination(shortName, trips):
	commonDest=True
	for orig in trips:
			if shortName not in [d.shortName for d in trips[orig].values()]:
				commonDest=False
	return commonDest

def encode(text):
    return text.encode('utf-8')
   	
def writeTripOptionsToFile(filename, trips, sortedShortNameList):
	f = open(filename+'.txt', 'w')
	for tup in sortedShortNameList:
		shortName=tup[0]
		price=tup[1]
		f.write("%s:%s" % (shortName, price))
		f.write("--Trips: ")
		for orig in trips:
			f.write(encode(trips[orig][shortName].toString()) + ", ")
		f.write("\n")
	f.close()

windowStart='20160401'
windowEnd='20160430'
trips = {}
originCities = ['JFK','LAX']
for orig in originCities:
	r = requests.get("https://www.kayak.com/h/explore/api?airport=%s&depart=%s&return=%s" % (orig, windowStart, windowEnd),headers={'User-Agent': 'curl -A "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5'})
	j = json.loads(r.text)
	tripOptions = {}
	for dest in j['destinations']:
		destObj = Destination(orig, dest['city']['name'], dest['country']['name'], dest['airport']['shortName'], dest['flightInfo']['url'], dest['depart'], dest['return'], dest['airline'], dest['flightInfo']['price'])
		tripOptions[destObj.shortName] = destObj
	trips[orig]=tripOptions

priceByDest={}
for orig in originCities:
	for shortName in trips[orig]:
		if not commonDestination(shortName, trips):
			continue
		if shortName in priceByDest:
			priceByDest[shortName]+=trips[orig][shortName].price
		else:
			priceByDest[shortName]=trips[orig][shortName].price
sorted_priceByDest = sorted(priceByDest.items(), key=itemgetter(1))

writeTripOptionsToFile("destinations", trips, sorted_priceByDest)
