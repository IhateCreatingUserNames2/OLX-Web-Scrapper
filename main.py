import requests
from bs4 import BeautifulSoup
import pandas as pd
import json


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None


def parse_json_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    script_tag = soup.find('script', id='__NEXT_DATA__')
    json_data = json.loads(script_tag.string)

    listings = []
    for item in json_data['props']['pageProps']['ads']:
        try:
            title = item.get('title', 'No title')
            price = item.get('price', 'No price')
            images = item.get('images', [])
            image = images[0]['originalWebP'] if images else 'No image'
            location = item.get('location', 'No location')
            category = item.get('category', 'Real Estate')
            properties = {prop['name']: prop['value'] for prop in item.get('properties', [])}
            rooms = properties.get('rooms', 'No rooms')
            bathrooms = properties.get('bathrooms', 'No bathrooms')
            garage_spaces = properties.get('garage_spaces', 'No garage spaces')
            re_features = properties.get('re_features', 'No features')

            listings.append({
                'Title': title,
                'Price': price,
                'Image': image,
                'Location': location,
                'Category': category,
                'Rooms': rooms,
                'Bathrooms': bathrooms,
                'Garage Spaces': garage_spaces,
                'Features': re_features
            })
        except Exception as e:
            print(f"Error parsing item: {e}")

    return listings


def main():
    url = 'https://www.olx.com.br/imoveis/aluguel'
    html = get_html(url)
    if html:
        listings = parse_json_data(html)
        if listings:
            df = pd.DataFrame(listings)
            df.to_csv('olx_real_estate_rentals.csv', index=False)
            print("Data has been exported to olx_real_estate_rentals.csv")
        else:
            print("No listings found.")
    else:
        print("Failed to retrieve the webpage.")


if __name__ == "__main__":
    main()
