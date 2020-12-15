# PurBeurre Project

About this project :
PurBeurre is an application who promotes healthier eating.
Note: all informations are requested from Open Food Facts (https://world.openfoodfacts.org/)

For this, it is based on two criteria:
* NOVA group: A classification in 4 groups to highlight the degree of processing of foods:
    from 1 (unprocessed or minimally processed foods) to 4 (ultra-processed food and drink products)
* NUTRI-SCORE: Indicates the nutritional quality of food:
    from A - dark green (good) to E - dark orange (bad)


# Files:
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
* Python3 (https://www.python.org/downloads/)
* MySQL (https://www.mysql.com/fr/downloads/)

__A MySQL user with permission is needed.__

See also https://www.digitalocean.com/community/tutorials/how-to-create-a-new-user-and-grant-permissions-in-mysql


# Program flow:
* Download PurBeurre
```
git clone https://github.com/RiwsPy/PurBeurre.git
```
* Open _PurBeurre_ folder
* Rename _.env.sample_ in _.env_
* Complete this file to permit a connection between the program and the locale database
* Launch program, execute this in the PurBeurre folder

    __Launch with database update__ (recommended for first use)
    ```
    pipenv install
    pipenv shell
    python3 main.py -uDB
    ```
    Your database will be completed or updated from OpenFoodFacts, its may take few seconds.

    __Launch without update__
    ```
    pipenv install
    pipenv shell
    python3 main.py
    ```
* Choose an option
    1. Find a product to substitute an other
        * Select product category
            * Select your product
                * Save (or not) product and the one proposed by PurBeurre
            * Back to parent folder
            * Quit PurBeurre
        * Back to parent folder
        * Quit PurBeurre
    2. Find your products previously saved
        * Back to parent folder
    3. Quit PurBeurre