# Projet PurBeurre

this project is under construction



About this project :
PurBeurre is an application who promotes healthier eating.
Note: all informations are requested from Open Food Facts (https://world.openfoodfacts.org/)

For this, it is based on two criteria:
* NOVA group: A classification in 4 groups to highlight the degree of processing of foods:
    from 1 (unprocessed or minimally processed foods) to 4 (ultra-processed food and drink products)
* NUTRI-SCORE: Indicates the nutritional quality of food:
    from A - dark green (good) to E - dark orange (bad)


Files:
- api/
    - locale.py (contains all constants for API)
    - openfoodfacts.py (contains requests to API)
- data/
    - category.py (class category)
    - product.py (class product)
- interface/
    - interface.py (contains method which allow the user to interact with interface)
- sql/
    - database.py (contains all sql requests)
    - tables_queries.sql (tables architecture to create tables in database)
- main.py
- .env.sample (file to configure SQL connection, NEED to be rename to .env)
- Pipfile.lock (contains all PurBeurre application dependencies)
- settings.py (active dotenv package)



# Prerequisites:
* Python (URL : ???)
* MySQL (URL : ???)

# Installation:
```
git clone https://github.com/RiwsPy/PurBeurre.git
cd PurBeurre/
pipenv install
pipenv shell
python3 main.py
```