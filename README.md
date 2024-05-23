WebScrapper para OLX - Imoveis e Veiculos,

Como usar: 
1) Rode o Arquivo main.py
2) Irá abrir uma UI
   2.1) Insira os dados necesseario: URL: Exemplo Veiculos: https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/estado-go / Imoveis: https://www.olx.com.br/imoveis/aluguel/estado-go
   2.2) Number of Pages = Número de Paginas que ele deve extrair. Exemplo: 5 = Vai exportar todos os Anuncios das 5 Paginas
   2.3) Category = Real State = Imoveis / Vehicles = Veiculos


Extrai em Imoveis: 
    'Title': title,
                'Price': price,
                'Image': image,
                'Location': location,
                'Category': category,
                'Rooms': rooms,
                'Bathrooms': bathrooms,
                'Garage Spaces': garage_spaces,
                'Features': re_features

Extrai em Veiculos: 
 listings.append({
                'Title': title,
                'Price': price,
                'Image': image,
                'Location': location,
                'Category': category,
                'Vehicle Model': vehicle_model,
                'Vehicle Brand': vehicle_brand,
                'Car Type': cartype,
                'Reg Date': regdate,
                'Mileage': mileage,
                'Motor Power': motorpower,
                'Fuel': fuel,
                'Gearbox': gearbox,
                'Car Steering': car_steering,
                'Car Color': carcolor,
                'Doors': doors,
                'End Tag': end_tag,
                'Owner': owner,
                'Financial': financial,
                'Warranty': warranty,
                'Has Auction': has_auction,
                'Is Settled': is_settled,
                'Is Funded': is_funded



Total de Paginas: 5 - Configuravel em: num_pages = 5 

Extrai para CSV 

