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
- data/
    - my.conf (user data for connect to database)
- interface/
    - interface.py (contains method which allow the user to interact with interface)
- database.py (connect and request data from Open Food Facts API)
- main.py (unused)
- tables_queries.sql (sql queries to create tables in database)
- Pipfile.lock (contains all PurBeurre application dependencies)



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