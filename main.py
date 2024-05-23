import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import tkinter as tk
from tkinter import messagebox


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


def main(base_url, num_pages):
    all_listings = []

    for page in range(1, num_pages + 1):
        url = f'{base_url}?o={page}'
        html = get_html(url)
        if html:
            listings = parse_json_data(html)
            if listings:
                all_listings.extend(listings)
                print(f"Page {page}: {len(listings)} listings found.")
            else:
                print(f"Page {page}: No listings found.")
        else:
            print(f"Failed to retrieve page {page}.")

    if all_listings:
        df = pd.DataFrame(all_listings)
        df.to_csv('olx_real_estate_rentals.csv', index=False)
        print("Data has been exported to olx_real_estate_rentals.csv")
        messagebox.showinfo("Success", "Data has been exported to olx_real_estate_rentals.csv")
    else:
        print("No listings found.")
        messagebox.showwarning("Warning", "No listings found.")


def start_scraping():
    base_url = entry_base_url.get()
    num_pages = int(entry_num_pages.get())
    main(base_url, num_pages)


# Create the tkinter UI
root = tk.Tk()
root.title("OLX Scraper")

tk.Label(root, text="Base URL:").grid(row=0, column=0, padx=10, pady=10)
entry_base_url = tk.Entry(root, width=50)
entry_base_url.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Number of Pages:").grid(row=1, column=0, padx=10, pady=10)
entry_num_pages = tk.Entry(root, width=10)
entry_num_pages.grid(row=1, column=1, padx=10, pady=10)

tk.Button(root, text="Start Scraping", command=start_scraping).grid(row=2, column=0, columnspan=2, pady=20)

root.mainloop()
