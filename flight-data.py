import urllib2
import json
import datetime


def request_flights(departure_date,return_date, departure_airport, arrival_airport):
	url = "http://terminal2.expedia.com/x/mflights/search?departureDate="+departure_date+"&returnDate="+return_date+"&departureAirport="+departure_airport+"&arrivalAirport="+arrival_airport+"&apikey=&maxOfferCount=2"
	json_text = json.load(urllib2.urlopen(url))
	fares_list = []
	flight_list = []
	fares = {'id':None,'price':None, 'url':None}
	flight_info = {'id':None, 'airline': None, 'departure_time': None, 'arrival_time':None}
	for offers in json_text['offers']:
			for legs in offers['legIds']:
				fares['id'] =  legs
				fares['price'] = offers['totalFare']
				fares['url'] = offers['detailsUrl']
				fares_list.append(fares.copy())

	for flight in json_text['legs']:
		flight_info['id'] = flight['legId'] 
		flight_info['airline']= flight['segments'][0]['airlineName']
		flight_info['departure_time']= flight['segments'][0]['departureTime']
		flight_info['arrival_time']= flight['segments'][0]['arrivalTime']
		flight_list.append(flight_info.copy())


	print '-------------------------------------------------'
	for i in fares_list:
		for j in flight_list:
			if i['id']== j['id']:
				print j.get('airline')
				print i.get('price')
				print j.get('departure_time')
				print j.get('arrival_time')
				#print i.get('url')
	print '-------------------------------------------------'

def populate_weekend_dates(start_index, ttl_duration):
    today = datetime.datetime.today().weekday()
    weekend_dates = []
    start= ''
    if(today==3 or today==4):
        start = datetime.datetime.now() + datetime.timedelta(days=3)
    else:
        start = datetime.datetime.now()
    #3 months into the future
    end =  (start + datetime.timedelta(ttl_duration*365/12))
    begin = start
    delta = datetime.timedelta(days=1)
    diff = 0
    #ONLY CALCULATE FRIDAY SINCE YOU CAN DO THE MATH FOR SUNDAY..
    weekend = ''
    if(start_index==4):
        weekend = set([3])
    elif(start_index==5):
        weekend = set([4])
    else:
        weekend = set([4])
    while(begin<=end):
            if(begin.weekday() in weekend):
                    weekend_dates.append(begin)
                    diff+=1
            begin+=delta
    return weekend_dates

def call_all_destinations(source, weekend_dates, dest, start_index):
        for d in dest:
            for date in weekend_dates:
                start_date = datetime.datetime.strftime(date,'%Y-%m-%d')
                end_date = ''
                if(start_index==4):
                    end_date = datetime.datetime.strftime(date+datetime.timedelta(3),'%Y-%m-%d')
                elif(start_index==5):
                    end_date = datetime.datetime.strftime(date+datetime.timedelta(2),'%Y-%m-%d')
                request_flights(start_date, end_date, source,dest)

call_all_destinations('ORD', populate_weekend_dates(4,1), 'LAX', 4)