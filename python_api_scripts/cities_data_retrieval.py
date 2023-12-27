# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
from citipy import citipy
from api_keys import weather_api_key

import pprint as pp

'''commented code left in script for debugging and testing purposes'''
lat_range = (-90, 90)
lng_range = (-180, 180)
lat = np.random.uniform(lat_range[0], lat_range[1], size=1500)

lon = np.random.uniform(lng_range[0], lng_range[1], size=1500)
lat_lngs = zip(lat, lon)

cities=[]
for coords in lat_lngs:
    latitude = coords[0]
    longitude = coords[1]
    #from citipy documentation https://github.com/wingchen/citipy
    location = citipy.nearest_city(latitude, longitude)
    # city nearest to randomly generated coordinates
    city_name=location.city_name
    # country code
    country_code=location.country_code

    ## print to make sure the city returned matches a country
    # print(city_name,',',country_code)

    # city/country combo seemed to be ok, but we only need to provide a city to the api, so this gets saved in a list to query later
    if city_name not in cities:
        cities.append(city_name)
#check count of cities
print(len(cities))

# # test json response for weather api
# # units='imperial'
# # weather_url=f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units={units}'
# # from api_keys import weather_api_key

# # test lat/lon for fairhope,alabama 30.5230° N, 87.9033° W
# weather_api_key="3974be9fa6e0d0ba48004fb47c9abbeb"
units='imperial'
api_key=weather_api_key
lat=30.5230
lon=-87.9033

## TEST ##
#weather api url
# url=f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units={units}'
# # url=f'https://api.openweathermap.org/data/2.5/weather?{params}'
# response=requests.get(url)
# fairhope_weather=response.json()
# print(response.url)
# pp.pprint(fairhope_weather)

# set up variables to use to loop through cities list
# info=fairhope_weather
# latitude=info['coord']['lat']
# longitude=info['coord']['lon']
# desc=info['weather'][0]['description']
# max_temp=info['main']['temp_max']
# humidity=info['main']['humidity']
# clouds=info['clouds']['all']
# wind = info['wind']['speed']
# # city_name=info['City']
# country=info['sys']['country']
# city_date=info['dt']
# # dictionary of retrieved data
# city_data_dict={
#     # "City Name": city_name,
#     "Country": country,
#     "City Lat":latitude,
#     "City Lon" :longitude,
#     "Max Temp" : max_temp,
#     "Wind": wind,
#     "City Date" : city_date,
#     "Humidity" : humidity,
#     "Clouds" : clouds,
#     "Description": desc,

# }
# pp.pprint(city_data_dict)
# exit()

'''gathering weather information in metric, will create conversion column to farenheit in jupyter notebook VacationPy'''
city_data=[]
record_groups=1
records_attempt=1
# loop through cities list and return dataframe of info
for index, city in enumerate(cities):
    records_attempt+=1
    if (index % 50 == 0 ) and (index >=50):        
        record_groups+1
        records_attempt=0
    # print(f'{city} is the {records_attempt} attempt and resulting datapoint for the {record_groups} group of api query attempted')


    # url call based on city name alone, no lat and lon required
    ## source: https://stackoverflow.com/questions/65373299/how-can-i-use-city-name-instead-of-lat-and-log-in-openweather-api
    # api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}
    base_url = f"http://api.openweathermap.org/data/2.5/weather?units=Metric&APPID={weather_api_key}"

    try:
        url=f'{base_url}&q={city}'
        # url=f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}'
        # url=f'https://api.openweathermap.org/data/2.5/weather?q={city}&APPID={weather_api_key}'
        response=requests.get(url)
        # print(response.url)
        info=response.json()
        # pp.pprint(info)
        # variables for curated information

        latitude=info['coord']['lat']
        # print(latitude)
        longitude=info['coord']['lon']
        # print(longitude)
        desc=info['weather'][0]['description']
        # print(desc)
        max_temp=info['main']['temp_max']
        # print(max_temp)
        humidity=info['main']['humidity']
        # print(humidity)
        clouds=info['clouds']['all']
        # print(clouds)
        wind = info['wind']['speed']
        # print(wind)        
        city_name=info['City']
        print(city_name)
        country=info['sys']['country']
        print(country)
        city_date=info['dt']
        # print(city_date)

        # dictionary 
        city_data_info={
            "City Name": city_name,
            "Country": country,
            "City Lat":latitude,
            "City Lon" :longitude,
            "Max Temp" : max_temp,
            "Wind": wind,
            "Date" : city_date,
            "Humidity" : humidity,
            "Cloudiness" : clouds,
            "Description": desc,

        }
        print(city_data_info)
        city_data.append(city_data_info)
        # print(city_name, country, wind)
        
    except:
        # print(f'url for {city} not found, skipping!')
        pass


        # print(city_data_dict)
        # city_data.append(city_data_dict)
    
    
print(city_data)
print('------------------------------------------------------------------')
print(f'found in total: {len(city_data)} different city weather records')
print('------------------------------------------------------------------')
print('sending to csv')
df=pd.DataFrame(city_data)
df.to_csv('output/cities_weather.csv',index_label="City_ID")





