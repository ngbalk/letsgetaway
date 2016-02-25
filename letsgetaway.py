import requests, json
from operator import itemgetter


class Destination:
	def __init__(self, cityName, countryName, shortName, kayakUrl, departDate, returnDate, airline, price):
		self.cityName = cityName
		self.countryName = countryName
		self.shortName = shortName
		self.kayakUrl = 'https://www.kayak.com'+kayakUrl
		self.departDate = departDate
		self.returnDate = returnDate
		self.airline = airline
		self.price = price
	def toString(self):
		return "%s, %s, %s, %s, %s, %s, %s" % (self.cityName, self.countryName, self.shortName, self.kayakUrl, self.departDate, self.returnDate, self.airline)
		
windowStart='20160401'
windowEnd='20160430'
trips = {}
originCities = ['JFK','LAX']
for orig in originCities:
	r = requests.get("https://www.kayak.com/h/explore/api?airport=%s&depart=%s&return=%s" % (orig, windowStart, windowEnd),headers={'User-Agent': 'curl -A "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5'})
	j = json.loads(r.text)
	tripOptions = []
	for dest in j['destinations']:
		destObj = Destination(dest['city']['name'], dest['country']['name'], dest['airport']['shortName'], dest['flightInfo']['url'], dest['depart'], dest['return'], dest['airline'], dest['flightInfo']['price'])
		tripOptions.append(destObj)
		# tripOptions.sort(key=lambda el: el.price)
		
		# tripOptions[dest['airport']['shortName']] = dest['flightInfo']['price']
	# tripOptions = sorted(tripOptions, key=itemgetter(2))
	trips[orig]=tripOptions

keyCity = originCities[0]
priceByDest={}
for orig in originCities:
	for dest, price in trips[orig].iteritems():
		commonDest = True
		for orig in originCities:
			if dest not in trips[orig].keys():
				commonDest = False
		if not commonDest:
			continue
		if dest in priceByDest:
			priceByDest[dest]+=price
		else:
			priceByDest[dest]=price
sorted_priceByDest = sorted(priceByDest.items(), key=itemgetter(1))

f = open('destinations.txt','w')
for item in sorted_priceByDest:
	f.write("%s %s\n" % (item[0], item[1]))
f.close()
