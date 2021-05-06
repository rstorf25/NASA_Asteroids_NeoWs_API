import requests
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


def get_data(start):
    key = open('key.txt', "r")
    api_key = key.read()
    end = start
    url = "https://api.nasa.gov/neo/rest/v1/feed?"
    response = requests.get(url + "start_date=" + start + "&end_date=" + end + "&api_key=" + str(api_key))
    data = response.json()
    return data

def extract_main(data, start_date):
    read_data = data['near_earth_objects'][start_date]
    return read_data

def select_data(data):
    zero = 0
    read_data = data
    dist_dict = dict()
    for i in range(len(read_data)):
        miss_distance = read_data[i]['close_approach_data'][zero]['miss_distance']['miles']
        miss_distance = float(miss_distance)
        miss_distance = round(miss_distance,2)
        velo = read_data[i]['close_approach_data'][zero]['relative_velocity']['miles_per_hour']
        velo = float(velo)
        velo = round(velo,2)
        size = read_data[i]['estimated_diameter']['feet']['estimated_diameter_max']
        size = float(size)
        size = round(size,2)
        ids = read_data[i]['id']
        name = read_data[i]['name']
        dangerous = read_data[i]['is_potentially_hazardous_asteroid']
        dangerous = str(dangerous)
        dist_dict[ids] = {'name':name, 'dangerous':dangerous, 'size (ft)':size, 'velocity (mph(':velo, 'miss_dist (mi)': miss_distance}

    return dist_dict

def dict_transform(data):
    for i in data:
        data[i]['dangerous'] = data[i]['dangerous'].replace('True', 'Dangerous')
        data[i]['dangerous'] = data[i]['dangerous'].replace('False', 'No Threat')
    return data

def pandas_transform(data):
    df = pd.DataFrame(data)
    df = df.transpose()
    df.columns = ['Name', 'Dangerous', 'Diameter (ft)', 'Velocity (mph)', 'Missed Earth Distance (mi)']
    df.index.name = 'ID'

    return df

def to_excel(data, output):
    df = pd.DataFrame(data)
    df.to_excel(output, sheet_name="NASA Asteroids")

def nasa_asteroids(date, output):

    data = get_data(date)

    extracted_data = extract_main(data,date)

    selected_data = select_data(extracted_data)

    rounded = dict_transform(selected_data)

    pandas_data = pandas_transform(rounded)

    to_excel(pandas_data, output)
    print("You have some Asteroid data!")

    return pandas_data

"""Example Use Found Below """
date = '1995-05-27'
output = r"C:\NASA_API\NASA_Asteroids.xlsx"

test = nasa_asteroids(date, output)


