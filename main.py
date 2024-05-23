import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import tkinter as tk
from tkinter import messagebox
import random


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


def parse_real_estate_data(json_data):
    listings = []
    for item in json_data['props']['pageProps']['ads']:
        try:
            title = item.get('title', 'Sem título')
            price = item.get('price', 'Sem preço')
            images = item.get('images', [])
            image = images[0]['originalWebP'] if images else 'Sem imagem'
            location = item.get('location', 'Sem localização')
            category = item.get('category', 'Imóveis')
            properties = {prop['name']: prop['value'] for prop in item.get('properties', [])}
            rooms = properties.get('rooms', 'Sem quartos')
            bathrooms = properties.get('bathrooms', 'Sem banheiros')
            garage_spaces = properties.get('garage_spaces', 'Sem vagas')
            re_features = properties.get('re_features', 'Sem características')

            listings.append({
                'Título': title,
                'Preço': price,
                'Imagem': image,
                'Localização': location,
                'Categoria': category,
                'Quartos': rooms,
                'Banheiros': bathrooms,
                'Vagas na garagem': garage_spaces,
                'Características': re_features
            })
        except Exception as e:
            print(f"Erro ao analisar item: {e}")

    return listings


def parse_vehicle_data(json_data):
    listings = []
    for item in json_data['props']['pageProps']['ads']:
        try:
            title = item.get('title', 'Sem título')
            price = item.get('price', 'Sem preço')
            images = item.get('images', [])
            image = images[0]['originalWebP'] if images else 'Sem imagem'
            location = item.get('location', 'Sem localização')
            category = item.get('category', 'Veículos')
            properties = {prop['name']: prop['value'] for prop in item.get('properties', [])}
            vehicle_model = properties.get('vehicle_model', 'Sem modelo')
            vehicle_brand = properties.get('vehicle_brand', 'Sem marca')
            cartype = properties.get('cartype', 'Sem tipo')
            regdate = properties.get('regdate', 'Sem data de registro')
            mileage = properties.get('mileage', 'Sem quilometragem')
            motorpower = properties.get('motorpower', 'Sem potência do motor')
            fuel = properties.get('fuel', 'Sem combustível')
            gearbox = properties.get('gearbox', 'Sem câmbio')
            car_steering = properties.get('car_steering', 'Sem direção')
            carcolor = properties.get('carcolor', 'Sem cor')
            doors = properties.get('doors', 'Sem portas')
            end_tag = properties.get('end_tag', 'Sem etiqueta de fim')
            owner = properties.get('owner', 'Sem proprietário')
            financial = properties.get('financial', 'Sem informações financeiras')
            warranty = properties.get('warranty', 'Sem garantia')
            has_auction = properties.get('has_auction', 'Sem leilão')
            is_settled = properties.get('is_settled', 'Sem liquidação')
            is_funded = properties.get('is_funded', 'Sem financiamento')

            listings.append({
                'Título': title,
                'Preço': price,
                'Imagem': image,
                'Localização': location,
                'Categoria': category,
                'Modelo do veículo': vehicle_model,
                'Marca do veículo': vehicle_brand,
                'Tipo de carro': cartype,
                'Data de registro': regdate,
                'Quilometragem': mileage,
                'Potência do motor': motorpower,
                'Combustível': fuel,
                'Câmbio': gearbox,
                'Direção': car_steering,
                'Cor': carcolor,
                'Portas': doors,
                'Etiqueta de fim': end_tag,
                'Proprietário': owner,
                'Informações financeiras': financial,
                'Garantia': warranty,
                'Leilão': has_auction,
                'Liquidação': is_settled,
                'Financiamento': is_funded
            })
        except Exception as e:
            print(f"Erro ao analisar item: {e}")

    return listings


def parse_json_data(html, category):
    soup = BeautifulSoup(html, 'html.parser')
    script_tag = soup.find('script', id='__NEXT_DATA__')
    json_data = json.loads(script_tag.string)

    if category == "Imóveis":
        return parse_real_estate_data(json_data)
    elif category == "Veículos":
        return parse_vehicle_data(json_data)
    else:
        return []


def main(base_url, num_pages, category):
    all_listings = []

    for page in range(1, num_pages + 1):
        url = f'{base_url}?o={page}'
        html = get_html(url)
        if html:
            listings = parse_json_data(html, category)
            if listings:
                all_listings.extend(listings)
                print(f"Página {page}: {len(listings)} anúncios encontrados.")
            else:
                print(f"Página {page}: Nenhum anúncio encontrado.")
        else:
            print(f"Falha ao recuperar a página {page}.")

    if all_listings:
        filename = f'olx_listings_{random.randint(1000, 9999)}.csv'
        df = pd.DataFrame(all_listings)
        df.to_csv(filename, index=False)
        print(f"Dados foram exportados para {filename}")
        messagebox.showinfo("Sucesso", f"Dados foram exportados para {filename}")
    else:
        print("Nenhum anúncio encontrado.")
        messagebox.showwarning("Aviso", "Nenhum anúncio encontrado.")


def start_scraping():
    base_url = entry_base_url.get()
    num_pages = int(entry_num_pages.get())
    category = category_var.get()
    main(base_url, num_pages, category)


# Create the tkinter UI
root = tk.Tk()
root.title("OLX Scraper")

tk.Label(root, text="URL Base:").grid(row=0, column=0, padx=10, pady=10)
entry_base_url = tk.Entry(root, width=50)
entry_base_url.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Número de Páginas:").grid(row=1, column=0, padx=10, pady=10)
entry_num_pages = tk.Entry(root, width=10)
entry_num_pages.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Categoria:").grid(row=2, column=0, padx=10, pady=10)
category_var = tk.StringVar(value="Imóveis")
tk.Radiobutton(root, text="Imóveis", variable=category_var, value="Imóveis").grid(row=2, column=1, sticky='w', padx=10,
                                                                                  pady=5)
tk.Radiobutton(root, text="Veículos", variable=category_var, value="Veículos").grid(row=3, column=1, sticky='w',
                                                                                    padx=10, pady=5)

tk.Button(root, text="Iniciar Scraping", command=start_scraping).grid(row=4, column=0, columnspan=2, pady=20)

root.mainloop()
