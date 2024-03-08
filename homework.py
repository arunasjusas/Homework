import requests
import pandas as pd

url = "http://homeworktask.infare.lt/search.php?from=MAD&to=AUH&depart=2024-03-11&return=2024-03-18"
response = requests.get(url)
json_data = response.json()
print(response)

flight_data = []
for journey in json_data['body']['data']['journeys']:
    for index, flight in enumerate(journey['flights']):
        for total in json_data['body']['data']['totalAvailabilities']:
            if journey['recommendationId'] == total['recommendationId']:
                data = {
                    'Departure': flight['airportDeparture']['code'],
                    'Departure Date': flight['dateDeparture'],
                    'Arrival': flight['airportArrival']['code'],
                    'Arrival Date': flight['dateArrival'],
                    'Flight Number': flight['companyCode'] + flight['number'],
                }
                if index < len(journey['flights']) - 1 and journey['flights'][index]['terminalArrival'] == 'Unique':
                    next_flight = journey['flights'][index + 1]
                    data['Next Departure'] = next_flight['airportDeparture']['code']
                    data['Next Departure Date'] = next_flight['dateDeparture']
                    data['Next Arrival'] = next_flight['airportArrival']['code']
                    data['Next Arrival Date'] = next_flight['dateArrival']
                else:
                    data['Price'] = total['total']
                    data['Taxes'] = journey['importTaxAdl']
                flight_data.append(data)

df = pd.DataFrame(flight_data)
print(df)
df.to_csv('flights_data.csv', index=False)
