
import csv
import requests
import os

local_cache = None
positionstack_api_key = os.environ.get('POSITIONSTACK_API')

def read_csv1_to_dict(csv_file):
    city_data = {}
    with open(csv_file, mode='r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            city_ascii = row['city_ascii']
            lat = float(row['lat'])
            lng = float(row['lng'])
            if city_ascii not in city_data:
                city_data[city_ascii] = (lat, lng)
    return city_data

def read_csv2_to_dict(csv_file):
    global local_cache

    with open(csv_file, mode='r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            country = row['country']
            lat = float(row['latitude'])
            lng = float(row['longitude'])
            local_cache[country] = (lat, lng)

def read_csv3_to_dict(csv_file):
    global local_cache

    with open(csv_file, mode='r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            state_name = row['name']
            lat = float(row['latitude'])
            lng = float(row['longitude'])
            local_cache[state_name] = (lat, lng)


def get_lat_lon(place_name):
    # Check if the place data exists in the dictionary
    if place_name in local_cache:
        print('Hit in local cache')
        return local_cache[place_name]
    else:
        # Make a remote HTTP API call to get the location data
        api_url = f"http://api.positionstack.com/v1/forward?access_key={positionstack_api_key}&query={place_name}"
        print(api_url)
        response = requests.get(api_url)
        if response.status_code == 200:
            resp = response.json()
            # print(resp)
            data = resp["data"]
            print(data[0])
            lat = float(data[0]["latitude"])
            lng = float(data[0]["longitude"])
            local_cache[place_name] = (lat, lng)
            return lat, lng
        else:
            print(f"Failed to fetch location data for {place_name}")
            return None, None


def reverse_geolocate(lat, lon):
    api_url = f"http://api.positionstack.com/v1/reverse?access_key={positionstack_api_key}&limit=2&query={lat},{lon}"
    response = requests.get(api_url)
    if response.status_code == 200:
        resp = response.json()
        print(resp)
        place_info = resp["data"][0]
        print(place_info)
        return place_info
    else:
        print(f"Failed to fetch location data for {lat}, {lon}")
        return None


def init():
    global local_cache
    local_cache = read_csv1_to_dict('./maps_data/worldcities.csv')
    read_csv2_to_dict('./maps_data/world_countries.csv')
    read_csv3_to_dict('./maps_data/us-states.csv')

init()
