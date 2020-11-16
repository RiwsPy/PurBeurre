"""

Has a method to connect and request data from Open Food Facts API

"""

# Comment partager my.conf et chiffrer le mdp ?

# pipenv install
# pipenv install mysql.connector
# pipenv shell

import mysql.connector
import requests
import json

class Database:
    def __init__(self):
        """ Configuration and connection to Database, configure 'data/my.conf' file """
        try:
            self.cnx = mysql.connector.connect(option_files='data/my.conf', option_groups=['connector_python'])
        except:
            print("Erreur lors de la connexion à la base de données.")
            return None

        print("Connexion à la base de données.")
        self.cursor = self.cnx.cursor()

        self.execute_sql_file_in_database('P5_db', 'tables_queries.sql')

        print("Déconnexion de la base de données.")
        self.cnx.close()
        # rows = cur.fetchall()

    def execute_sql_file_in_database(self, database, filename):
        """
            Execute filename in database like a SOURCE command
            param database: database name
            param filename: file name to load (must be in the same folder)
            type database: str
            type filename: str
            return: query return
            rtype: list
        """
        self.cursor.execute("USE " + database)

        #self.cursor.execute("DROP TABLE IF EXISTS Favorite_products")
        #self.cursor.execute("DROP TABLE IF EXISTS Products")
        #self.cursor.execute("DROP TABLE IF EXISTS Category")

        
        with open(filename, 'r') as bdd:
            sql_queries = bdd.read().split(';')

        for query in sql_queries[:-1]: # last value is ignored
            try:
                self.cursor.execute(query)
            #except mysql.connector.errors.DatabaseError: # table already exists
            #    pass
            except mysql.connector.Error as error:
                print(error)

        self.cursor.execute("SHOW TABLES") # test
        return self.cursor.fetchall()
        #self.cnx.commit()
        

    def close(self):
        """ Close connection """
        self.cnx.close()

    def call_api(self):
        """ Request and import data from Open Food Facts API """

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




if __name__ == "__main__":
    conn = Database()
