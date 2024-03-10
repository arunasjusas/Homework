import requests
import pandas as pd

url = "http://homeworktask.infare.lt/search.php?from=MAD&to=AUH&depart=2024-03-13&return=2024-03-22"
response = requests.get(url)
json_data = response.json()

flight_data = []
for journey in json_data['body']['data']['journeys']:
    for index, flight in enumerate(journey['flights']):
        for total in json_data['body']['data']['totalAvailabilities']:
            if journey['recommendationId'] == total['recommendationId']:
                if index == 0:
                    data = {
                        'Price': total['total'],
                        'Taxes': journey['importTaxAdl'],
                        'Departure': flight['airportDeparture']['code'],
                        'Departure Date': flight['dateDeparture'],
                        'Arrival': flight['airportArrival']['code'],
                        'Arrival Date': flight['dateArrival'],
                        'Flight Number': flight['companyCode'] + flight['number']
                    }
                else:
                    data.update({
                        'Leg': 'Second',
                        'Second Departure': flight['airportDeparture']['code'],
                        'Second Departure Date': flight['dateDeparture'],
                        'Second Arrival': flight['airportArrival']['code'],
                        'Second Arrival Date': flight['dateArrival'],
                        'Second Flight Number': flight['companyCode'] + flight['number']
                    })
                flight_data.append(data)

df = pd.DataFrame(flight_data)
print(df)
df.to_csv('flights_without_connections.csv', index=False)
