"""

Request and import data from Open Food Facts API

"""

import requests
import json
from data.product import Product
from data.category import Category
from api.locale import HEADERS, URL

def call_api(bdd):
    headers={"User-Agent":HEADERS}
    payload = {
        'action': 'process',
        'tagtype_0': 'categories',
        'tag_contains_0': 'contains',
        'tag_0': 'Boisson', # à mod
        'tagtype_1': 'countries',
        'tag_contains_1': 'contains',
        'tag_1': 'France',
        'tagtype_2': 'categories_lc',
        'tag_contains_2': 'contains',
        'tag_2': 'fr',
        'sort_by': 'unique_scans_n', # sort by popularity
        'page_size': 20, # possible choice : 20, 50, 100, 250, 500, 1000
        'page': 1,
        'json': True,

    }

    print("Work in progress")
    req = requests.get(URL, params=payload, headers=headers)
    results_json = req.json()
    #with open('request_save.txt', 'w') as fichier:
    #    json.dump(results_json, fichier, indent=5)
    #print(results_json)

    columns = ["code", "product_name_fr", "nutrition_grades", "nova_groups", "stores", "categories"]

    for product in results_json["products"]:
        add = True
        save_info = []
        for column_name in columns:
            if not column_name in product: # parfois les données sont incomplètes, dans ce cas le produit est ignoré
                add = False
                break
            save_info.append(product[column_name])
        if add:
            pro = Product()
            code = pro.add(bdd, save_info)
            cat = Category()
            list_id_cat = cat.add(bdd, product["categories"])

            for id_cat in list_id_cat:
                bdd.add_assoc_pro_cat(code, id_cat)



