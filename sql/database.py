"""

Class Database
Has a method to connect and request data from sql database

"""

# pipenv install
# pipenv install mysql.connector
# pipenv shell

import mysql.connector
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

        if self.init_connection():
            self.create_database()
            self.execute_sql_file_in_database('tables_queries.sql')

            # rows = cur.fetchall()
            #self.close_connection()

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

        #self.execute("DROP TABLE IF EXISTS Assoc_product_category")
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

    def execute(self, query, data = None):
        try:
            self.cursor.execute(query, data)
        except mysql.connector.Error as error:
            print(error)
            return False

        return True

    def init_connection(self):
        """ Open connection """

        print("Connexion à la base de données.")

        try:
            self.cnx = mysql.connector.connect(
                database=self.bd_name,
                user=self.bd_user,
                password=self.bd_password
                )
            self.cursor = self.cnx.cursor()
            #self.cnx = mysql.connector.connect(option_files='data/my.conf', option_groups=['connector_python'])
        except:
            print("Erreur lors de la connexion à la base de données.")
            return False

        return True

    def close_connection(self):
        """ Close connection """
        print("Déconnexion de la base de données.")
        self.cnx.close()

    def add_product(self, product):
        """
            Add a product in Product table
            param product: list with 6 parameters :
                code, product_name, nova_score, nutrition_score, store_name, categories
            type product: list
            return: product code
            rtype: str
        """
        # vérification de la connection ?
        # vérification des informations ?

        add_line = "INSERT INTO Products (code, product_name, nova_score, nutrition_score, store_name) \
            VALUES (%s, %s, %s, %s, %s)"
        data_line = (product[0], product[1], product[2], product[3], product[4])
        self.execute(add_line, data_line)

        return product[0] # code

    def add_category(self, name):
        category_id = self.category_name_to_id(name)
        if not category_id:
            add_line = "INSERT INTO Category (category_name) \
                VALUES (%s)"
            data_line = (name[:100],)
            self.execute(add_line, data_line)
            category_id = self.category_name_to_id(name) # moyen plus rapide ?

        return category_id[0][0]

    def category_name_to_id(self, name):
        add_line = "SELECT id FROM Category WHERE category_name = %s"
        data_line = (name,)
        self.execute(add_line, data_line)
        return self.cursor.fetchall()

    def add_assoc_pro_cat(self, code_pro, cat_id):
        add_line = "INSERT INTO Assoc_product_category (code, id) \
            VALUES (%s, %s)"
        data_line = (code_pro, cat_id)
        self.execute(add_line, data_line)

if __name__ == "__main__":
    conn = Database()
