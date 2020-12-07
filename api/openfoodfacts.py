"""

Request and import data from Open Food Facts API

"""

import requests
from data.product import Product
from data.category import Category
from api.locale import HEADERS, URL_SEARCH, CATEGORIES, PAYLOAD


def call_api(bdd):
    """
        Request Open Food Facts API
        Save the results in the database
        param bdd: database
        type bdd: database.Database
        return: None
    """

    headers = {"User-Agent": HEADERS}
    code_set = set()
    print("Mise à jour de la base de données...")
    params = PAYLOAD.copy()

    for index, category in enumerate(CATEGORIES):
        params["tag_0"] = category
        req = requests.get(URL_SEARCH, params=params, headers=headers)
        results_json = req.json()

        cat = Category(bdd, category, index)
        cat.add()

        for product_info in results_json["products"]:
            if not product_info["code"] in code_set:
                code_set.add(product_info["code"])
                pro = Product(bdd)
                pro.cleaner(product_info)
                pro.add()
                bdd.add_assoc_pro_cat(pro, index)
