"""

Request and import data from Open Food Facts API

"""


import requests
import json


def call_api(self):
    search_url = "https://fr.openfoodfacts.org/cgi/search.pl?"
    headers = {"User-Agent": "P5_PurBeurre - Version 0.1"}
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
    req = requests.get(search_url, params=payload, headers=headers)
    results_json = req.json()
    with open('request_save.txt', 'w') as fichier:
        json.dump(results_json, fichier, indent=5)
    #print(results_json)

