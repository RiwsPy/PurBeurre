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
            """
            self.clear_all_tables()
            self.execute_sql_file_in_database('sql/tables_queries.sql')
            """

    def create_database(self):
        self.execute("CREATE DATABASE IF NOT EXISTS " + self.bd_name)
        self.execute("USE " + self.bd_name)

    def execute_sql_file_in_database(self, filename):
        """
            Execute filename in database like a SOURCE command
            param filename: file name to load (must be in the root folder)
            type filename: str
            return: query return
            rtype: list
        """

        with open(filename, 'r') as bdd:
            sql_queries = bdd.read().split(';')

        for query in sql_queries[:-1]: # last value is ignored
            self.execute(query)

    def clear_all_tables(self):
        """
            Drop all table in database
        """
        self.execute("DROP TABLE IF EXISTS Assoc_product_category")
        self.execute("DROP TABLE IF EXISTS Favorite_product")
        self.execute("DROP TABLE IF EXISTS Product")
        self.execute("DROP TABLE IF EXISTS Category")

    def execute(self, query, data = None):
        # you must commit the data after a sequence of INSERT, DELETE, and UPDATE statements.
        # See : https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html

        need_commit = False
        first_statement = query.split(" ")[0].upper()
        if first_statement in ["INSERT", "DELETE", "UPDATE"]:
            need_commit = True

        try:
            self.cursor.execute(query, data)
            if need_commit:
                self.cnx.commit()
        except mysql.connector.Error as error:
            print(error)
            if need_commit:
                self.cnx.rollback()
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
        self.cursor.close()
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
        # vérification de la connexion ?
        # vérification des informations ?

        add_line = "INSERT INTO Product \
            (code, product_name, nova_score, nutrition_score, store_name) \
            VALUES (%s, %s, %s, %s, %s)"
        data_line = (product[0], product[1], product[2], product[3], product[4])
        self.execute(add_line, data_line)

        return product[0] # code

    def add_category(self, name, index):
        add_line = "INSERT INTO Category (id, category_name) \
            VALUES (%s, %s)"
        data_line = (index, name[:100])
        self.execute(add_line, data_line)

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

    def create_index_nova_nutri_score(self):
        self.execute("ALTER TABLE Product ADD INDEX ind_nova_nutri\
            (nova_score, nutrition_score)") # index creation

    def all_categories_name(self):
        self.execute("SELECT category_name FROM Category")
        return self.cursor.fetchall()

    def all_info_product(self, code_product):
        add_line = "SELECT product_name, code, nova_score, nutrition_score, store_name\
        FROM Product WHERE code = %s"
        data_line = (code_product,)
        self.execute(add_line, data_line)
        return self.cursor.fetchall()

    def all_products_in_category(self, cat):
        self.execute("SELECT p.product_name, p.code, p.nova_score, p.nutrition_score, p.store_name\
            FROM Product AS p\
            INNER JOIN Assoc_product_category AS a\
                ON a.code = p.code\
            WHERE a.id = %s\
            ORDER BY nova_score, nutrition_score, code", (cat,))
        return self.cursor.fetchall()

    def all_favorite_product(self):
        add_line = "SELECT code, substitute_code FROM Favorite_product"
        self.execute(add_line)
        return self.cursor.fetchall()

    def save_product(self, product_code, substitute_code):
        add_line = "INSERT INTO Favorite_product (code, substitute_code) VALUES (%s, %s)"
        data_line = (product_code, substitute_code)
        self.execute(add_line, data_line)

if __name__ == "__main__":
    conn = Database()
