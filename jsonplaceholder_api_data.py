
import requests
import pandas as pd


def get_data_from_get_api(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return {"response": "no response"}
    except requests.exceptions.RequestException as e:
        print(f"An error occured {e}")


url = "https://jsonplaceholder.typicode.com/users"
photos_url = "https://jsonplaceholder.typicode.com/photos"


def data_to_csv():

    data = get_data_from_get_api(url)

    data = pd.json_normalize(data)

    data.apply(
        lambda row: f"{row['address.street']}, {row['address.suite']}, {row['address.city']}	{row['address.zipcode']}", axis=1)

    data['address'] = data.apply(
        lambda row: f"{row['address.street']}, {row['address.suite']}, {row['address.city']}	{row['address.zipcode']}", axis=1)

    data = data.drop(columns=['address.street', 'address.suite', 'address.city',
                              'address.zipcode', 'address.geo.lat',	'address.geo.lng'])

    data = data.drop(columns=['company.catchPhrase', 'company.bs'])

    data = data.rename(columns={"company.name": "company_name"})

    photo_data = get_data_from_get_api(photos_url)

    photo_data = pd.json_normalize(photo_data)

    clean_df = photo_data.join(data.set_index(
        'id'), on='id', how='inner', lsuffix='_photo', rsuffix='_user')

    final_df = clean_df.drop(['albumId', 'title', 'thumbnailUrl'], axis=1)

    final_df.to_csv('data.csv', index=False)
