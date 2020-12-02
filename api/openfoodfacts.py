"""

Request and import data from Open Food Facts API

"""

import requests
from data.product import Product
from data.category import Category
from api.locale import HEADERS, URL_SEARCH, CATEGORIES, PAYLOAD, FIELDS

def call_api(bdd):
    headers={"User-Agent":HEADERS}
    code_set = set()
    print("Mise à jour de la base de données...")

    for index, category in enumerate(CATEGORIES):
        param = PAYLOAD.copy()
        param["tag_0"] = category
        req = requests.get(URL_SEARCH, params=param, headers=headers)
        results_json = req.json()

        cat = Category(category, index)
        cat.add(bdd)        

        for product in results_json["products"]:
            if not product["code"] in code_set:
                code_set.add(product["code"])
                add = True
                save_info = []
                for field in FIELDS:
                    if not field in product:
                        add = False
                        break
                    save_info.append(product[field])

                if add: # add a product if it has all fields
                    pro = Product()
                    code = pro.add(bdd, save_info)

                    bdd.add_assoc_pro_cat(code, index)

    bdd.create_index_nova_nutri_score()
