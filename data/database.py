"""

Class Database
Has a method to connect and request data from Open Food Facts API

"""

# pipenv install
# pipenv install mysql.connector
# pipenv shell

import mysql.connector
import requests
import json
import os
import settings

class Database:
    def __init__(self):
        """ For configurate and connect to Database, configure '.env' file """

        self.bd_name = os.getenv("DATABASE")
        self.bd_user = os.getenv("SQL_USER")
        self.bd_password = os.getenv("SQL_PASSWORD")
        self.cnx = None
        self.cursor = None

        print("Connexion à la base de données.")
        self.init_connection()

        if self.cursor:
            self.create_database()
            result = self.execute_sql_file_in_database('tables_queries.sql')
            print(result) # test

            # rows = cur.fetchall()
            self.close_connection()

    def create_database(self):
        self.execute("CREATE DATABASE IF NOT EXISTS " + self.bd_name)

    def execute_sql_file_in_database(self, filename):
        """
            Execute filename in database like a SOURCE command
            param filename: file name to load (must be in the root folder)
            type filename: str
            return: query return
            rtype: list
        """
        self.execute("USE " + self.bd_name)

        #self.execute("DROP TABLE IF EXISTS Favorite_products")
        #self.execute("DROP TABLE IF EXISTS Products")
        #self.execute("DROP TABLE IF EXISTS Category")

        with open(filename, 'r') as bdd:
            sql_queries = bdd.read().split(';')

        for query in sql_queries[:-1]: # last value is ignored
            self.execute(query)

        self.execute("SHOW TABLES") # test
        return self.cursor.fetchall()
        #self.cnx.commit()

    def execute(self, query):
        try:
            self.cursor.execute(query)
            return True
        except mysql.connector.Error as error:
            print(error)

        return False

    def init_connection(self):
        """ Open connection """

        try:
            self.cnx = mysql.connector.connect(
                database=self.bd_name,
                user=self.bd_user,
                password=self.bd_password
                )
            self.cursor = self.cnx.cursor()
            return True
            #self.cnx = mysql.connector.connect(option_files='data/my.conf', option_groups=['connector_python'])
        except:
            print("Erreur lors de la connexion à la base de données.")

        return False

    def close_connection(self):
        """ Close connection """
        print("Déconnexion de la base de données.")
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
