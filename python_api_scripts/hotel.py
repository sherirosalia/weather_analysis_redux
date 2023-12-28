
import pandas as pd
import requests
import pprint as pp
from api_keys import geoapify_key
# print(geoapify_key)



'''code commented out below is for testing purposes. Queries api on a single location (Fairhope,AL) test'''

# categories='accommodation.hotel'
# radius=10000        
# latitude=30.694666
# longitude=-87.877546
# limit=3

# fairhope_url=f"https://api.geoapify.com/v2/places?categories={categories}&filter=circle:{longitude},{latitude},{radius}&bias=proximity:{longitude},{latitude}&limit={limit}&apiKey={geoapify_key}"

# response = requests.get(fairhope_url)
# fairhope_data=response.json()
# counter=3
# # pp.pprint(data['features'][1])
# hotel_counter=0
# hotel_count_limit=5
# for x in fairhope_data['features']:
#     hotel_counter+=1
#     if hotel_counter <= hotel_count_limit:
#         name=x['properties']['name']

#         pp.pprint(name)


''' Get hotels near cities which was created in cities_data_retrieval.py,
this file has more information than the similarly named created in Jupyter Notebook'''
csv=pd.read_csv('python_api_scripts/output/cities_weather.csv', index_col=False)
df=pd.DataFrame(csv)
# print(df.sample())

curated=df.loc[(df['Max Temp']>= 50) & (df['Max Temp'] <72)]
# print(len(curated))

curated.to_csv('python_api_scripts/output/curated_cities.csv', index=False)
selected_df=pd.read_csv('python_api_scripts/output/curated_cities.csv', index_col=None)
print(selected_df.sample())


# print(f'count of cities csv: {len(selected_df)}')
# print(selected_df.sample(3))
print(selected_df.columns)

## send to csv file
# selected_df.to_csv('python_api_scripts/output/curated_cities.csv')

categories='accommodation.hotel'
radius=100000        
limit=5


hotel_list=[]
for index, row in selected_df.iterrows():
    # print(index)
    # print(row)
    city_id=row['City_ID']
    temp=row['Max Temp']
    description=row['Description']
    latitude=row['City Lat']
    longitude=row['City Lon']
    url=f"https://api.geoapify.com/v2/places?categories={categories}&filter=circle:{longitude},{latitude},{radius}&bias=proximity:{longitude},{latitude}&limit={limit}&apiKey={geoapify_key}"
    response=requests.get(url)
    retrieved_url=response.url
    data=response.json()
    # print(retrieved_url)
    # pp.pprint(data)

    # restrict to two hotels with best quality data
    hotel_counter=0
    hotel_count_limit=1
    for x in data['features']:
        
        
        if hotel_counter <= hotel_count_limit:
            try:
                name=x['properties']['name']
            except:
                pass
            try:
                address=x['properties']['address_line2']
                # place_id=x['place_id']
                city=x['properties']['city']
                country=x['properties']['country']
                lat=x['properties']['lat']
                lng=x['properties']['lon']
                try:
                    phone=x['properties']['datasource']['raw']['phone']
                except:
                    phone='phone not provided'
                    
                try:
                    email=x['properties']['datasource']['raw']['website']
                except:
                    email='email not provided'
                    
                try:
                    web=x['properties']['datasource']['raw']['website']
                except:
                    web='website not provided'
                
                hotel_info_dict={
                    'Hotel Name':name,
                    'Hotel City':city,
                    'Hotel Country':country,
                    'Hotel Phone':phone,
                    'Hotel Website':web,
                    'Hotel Email':email,
                    'Hotel Latitude':lat,
                    'Hotel Longitude':lng,
                    'Weather' : description,
                    'City_Id'  : city_id,
                    'Temperature' :temp,   
                    
                }

                print(hotel_info_dict)
                hotel_list.append(hotel_info_dict)
                hotel_counter+=1
            except:
                print('no hotels found')
                pass
                
            
### export hotels information to CSV to be displayed in Leaflet, see app.js file
hotel_df=pd.DataFrame(hotel_list)
print(hotel_df.sample(5))
print('sending to csv')
hotel_df.to_csv('python_api_scripts/output/hotels_near_cities.csv')




  