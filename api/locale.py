URL_SEARCH = "https://fr.openfoodfacts.org/cgi/search.pl?"
URL_PRODUCT = "https://fr.openfoodfacts.org/product"
HEADERS = "P5_PurBeurre - Version 0.1"


CATEGORIES = [
    "Petit-déjeuners",
    "Légumes et dérivés",
    "Céréales et pommes de terre",
    "Plats préparés",
    "Desserts",
    "Boissons"]

PAYLOAD = {
    'action': 'process',
    'tagtype_0': 'categories',
    'tag_contains_0': 'contains',
    'tag_0': '',  # category
    'tagtype_1': 'countries',
    'tag_contains_1': 'contains',
    'tag_1': 'France',
    'tagtype_2': 'categories_lc',
    'tag_contains_2': 'contains',
    'tag_2': 'fr',
    'sort_by': 'unique_scans_n',  # sort by popularity
    'page_size': 50,  # possible choice : 20, 50, 100, 250, 500, 1000
    'page': 1,
    'json': True,
}

FIELDS = [
    "code",
    "product_name_fr",
    "nova_groups",
    "nutrition_grades",
    "stores",
    "categories"]
